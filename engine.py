import os
import sys

from PySide6.QtCore import QObject, Signal, QProcess, QUrl, QThread
from PySide6.QtGui import QDesktopServices

from moviepy.editor import *

def resource_path(*relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, *relative_path)

ffmpeg_path = resource_path('ffmpeg','ffmpeg.exe')
rife_path = resource_path('rife','rife-ncnn-vulkan.exe')
rife_model_path = resource_path('rife','rife-v4.6')
realesrgan_path = resource_path('realesrgan','realesrgan-ncnn-vulkan.exe')
realesrgan_model_path = resource_path('realesrgan','models')

class ReadThread(QThread):
    done = Signal(str)

    def __init__(self, input_path, frames_path):
        super().__init__()
        self.input_path = input_path
        self.frames_path = frames_path

    def run(self):
        video = VideoFileClip(self.input_path)
        fps = video.fps
        num_frames = int(video.duration * video.fps)
        print('fps', fps, 'frames', num_frames)

        video.write_images_sequence(os.path.join(self.frames_path,'frame%08d.png'))
        video.close()

        self.done.emit(f'{fps} {num_frames}')

class WriteThread(QThread):
    done = Signal(str)

    def __init__(self, input_path, up_path, output_path, fps, form):
        super().__init__()
        self.input_path = input_path
        self.up_path = up_path
        self.output_path = output_path
        self.fps = fps
        self.form = form

    def run(self):
        video_up = ImageSequenceClip(self.up_path, fps=self.fps)
        video = VideoFileClip(self.input_path)

        video_up.set_audio(video.audio)
        if self.form.lower() == 'gif':
            video_up.write_gif(self.output_path)
        else:
            video_up.write_videofile(self.output_path)

        video_up.close()
        video.close()

        self.done.emit(f'Done')

class Client_Engine(QObject):
    status = Signal(str)

    def __init__(self):
        super().__init__()

        self.process2 = QProcess()
        self.process2.readyReadStandardError.connect(self.do_read2)
        self.process2.finished.connect(self.do_step3)
        self.process2.errorOccurred.connect(self.do_error2)

        self.process3 = QProcess()
        self.process3.readyReadStandardError.connect(self.do_read3)
        self.process3.finished.connect(self.do_step4)
        self.process3.errorOccurred.connect(self.do_error3)
        self.param = {'total':0}

    def do_generate(self, param):
        self.param.update(param)

        # print(param['input'])
        # print(param['output'])

        if len(self.param['input'])<1: 
            if self.param['open'] and self.param['output']:
                QDesktopServices.openUrl(QUrl(f"file:///{param['output']}",QUrl().TolerantMode))
            return

        self.input_path = self.param['input'][0]
        self.param['input'] = self.param['input'][1:]

        basename = os.path.basename(self.input_path)
        self.form = basename.split('.')[-1]
        output_path = basename[:-len(self.form)-1]+'_anime2x.'+self.form
        self.output_path = os.path.join(param['output'], output_path)

        self.do_step1()

    def do_step1(self):
        """
        Extract frames
        """
        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] " + "Extracting Frames.") 

        self.frames_path = os.path.join(self.param['output'], 'frames')
        os.makedirs(self.frames_path, exist_ok=True)

        self.read_thread = ReadThread(self.input_path, self.frames_path)
        self.read_thread.start()
        self.read_thread.done.connect(self.do_step2)

    def do_step2(self, info:str):
        """
        Interpolate frames
        """
        fps, num_frames = info.split()
        self.fps = float(fps)
        self.num_frames = int(num_frames)

        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] " + f"Processing a video with {num_frames} frames and {fps} fps.")

        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] " + "Interpolating Frames.")

        if self.param['inter'] > 1:
            self.inter_path = self.frames_path + "_inter"
            os.makedirs(self.inter_path, exist_ok=True)
            engine = rife_path
            args = [f" -m \"{rife_model_path}\" ",
                    f" -i \"{self.frames_path}\" ",
                    f" -o \"{self.inter_path}\" ",
                    f" -n \"{self.num_frames * self.param['inter']}\" "]
            self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] Running"+f"\"{engine}\""+' '.join(args))
            self.process2.startCommand(f"\"{engine}\""+' '.join(args))
        else:
            self.inter_path = self.frames_path
            self.do_step3()

    def do_step3(self):
        """
        Upsample frames
        """
        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] " + "Upsampling Frames.")

        if self.param['up'] > 1:
            self.up_path = self.frames_path + "_up"
            os.makedirs(self.up_path, exist_ok=True)
            engine = realesrgan_path
            args = [f" -m \"{realesrgan_model_path}\" ",
                    f" -n \"realesr-animevideov3\" " ,
                    f" -i \"{self.inter_path}\" ",
                    f" -o \"{self.up_path}\" ",
                    f" -s \"{self.param['up']}\" "]
            self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] Running"+f"\"{engine}\""+' '.join(args))
            self.process3.startCommand(f"\"{engine}\""+' '.join(args))
        else:
            self.up_path = self.inter_path
            self.do_step4()

    def do_step4(self):
        """
        Concatenate frames
        """   
        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] " + "Concatenating Frames.") 

        self.write_thread = WriteThread(self.input_path, self.up_path, self.output_path, self.fps * self.param['inter'], self.form)
        self.write_thread.start()
        self.write_thread.done.connect(self.do_finish)

    def do_finish(self, info):
        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] Finished with {len(self.param['input'])} left.")
        self.do_generate(self.param)

    def do_error2(self):
        self.status.emit("[ERROR] Process failed:"+ self.process2.errorString())

    def do_error3(self):
        self.status.emit("[ERROR] Process failed:"+ self.process3.errorString())

    def do_read2(self):
        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] "+self.process2.readAllStandardError().data().decode().strip())

    def do_read3(self):
        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] "+self.process3.readAllStandardError().data().decode().strip())

    def do_cancel(self):
        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] Trying kill process.")

        self.process2.kill()
        self.process2.terminate()

        self.process3.kill()
        self.process3.terminate()
