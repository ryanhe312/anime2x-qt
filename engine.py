import os, re, datetime
import sys

from PySide6.QtCore import QObject, Signal, QProcess, QUrl
from PySide6.QtGui import QDesktopServices

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

class Client_Engine(QObject):
    status = Signal(str)

    def __init__(self):
        super().__init__()
        self.process1 = QProcess()
        self.process1.readyReadStandardError.connect(self.do_read1)
        self.process1.finished.connect(self.do_step2)
        self.process1.errorOccurred.connect(self.do_error1)

        self.process2 = QProcess()
        self.process2.readyReadStandardError.connect(self.do_read2)
        self.process2.finished.connect(self.do_step3)
        self.process2.errorOccurred.connect(self.do_error2)

        self.process3 = QProcess()
        self.process3.readyReadStandardError.connect(self.do_read3)
        self.process3.finished.connect(self.do_step4)
        self.process3.errorOccurred.connect(self.do_error3)

        self.process4 = QProcess()
        self.process4.readyReadStandardError.connect(self.do_read4)
        self.process4.finished.connect(self.do_finish)
        self.process4.errorOccurred.connect(self.do_error4)
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
        self.name = basename.split('.')[-2]
        self.form = basename.split('.')[-1] if param["form"] is None else param["form"]
        output_path = basename[:-len(self.form)-1]+'_anime2x.'+self.form
        self.output_path = os.path.join(param['output'], output_path)

        self.do_step1()

    def do_step1(self):
        """
        Extract frames
        """
        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] " + "Extracting Frames.") 

        self.frames_path = os.path.join(self.param['output'], f'{self.name}_{datetime.datetime.now().strftime("%a_%b_%d_%H_%M")}_frames')
        os.makedirs(self.frames_path, exist_ok=True)

        engine = ffmpeg_path
        args = [f" -i \"{self.input_path}\" ",
                f" -pix_fmt rgb24  \"{os.path.join(self.frames_path,'%08d.png')}\" "]
        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] Running"+f"\"{engine}\""+' '.join(args))
        self.process1.startCommand(f"\"{engine}\""+' '.join(args))

    def do_step2(self):
        """
        Interpolate frames
        """
        self.num_frames = len(os.listdir(self.frames_path))

        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] " + f"Processing a video with {self.num_frames} frames and {self.fps} fps.")

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

        if self.form.lower() == 'gif':
            engine = ffmpeg_path
            args = [f" -y -framerate {self.fps * self.param['inter']}",
                    f" -i \"{os.path.join(self.up_path,'%08d.png')}\" ",
                    f" \"{self.output_path}\" "]
        else:
            engine = ffmpeg_path
            args = [f" -y -framerate {self.fps * self.param['inter']}",
                    f" -i \"{os.path.join(self.up_path,'%08d.png')}\" ",
                    f" -i \"{self.input_path}\" ",
                    f" -c:v libx264 -pix_fmt yuv420p -map 0:v:0 -map 1:a:0? ",
                    f" \"{self.output_path}\" "]
        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] Running"+f"\"{engine}\""+' '.join(args))
        self.process4.startCommand(f"\"{engine}\""+' '.join(args))

    def do_finish(self):
        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] Finished with {len(self.param['input'])} left.")
        self.do_generate(self.param)

    def do_error1(self):
        self.status.emit("[ERROR] Process failed:"+ self.process1.errorString())

    def do_error2(self):
        self.status.emit("[ERROR] Process failed:"+ self.process2.errorString())

    def do_error3(self):
        self.status.emit("[ERROR] Process failed:"+ self.process3.errorString())

    def do_error4(self):
        self.status.emit("[ERROR] Process failed:"+ self.process4.errorString())

    def do_read1(self):
        info = self.process1.readAllStandardError().data().decode().strip()
        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] "+info)
        fps = re.search(r'([0-9\.]+) fps,' ,info)
        if fps:
            self.fps = float(fps.group(1))

    def do_read2(self):
        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] "+self.process2.readAllStandardError().data().decode().strip())

    def do_read3(self):
        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] "+self.process3.readAllStandardError().data().decode().strip())

    def do_read4(self):
        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] "+self.process4.readAllStandardError().data().decode().strip())

    def do_cancel(self):
        self.status.emit(f"[INFO {self.param['total']-len(self.param['input'])}/{self.param['total']}] Trying kill process.")

        self.process1.kill()
        self.process1.terminate()

        self.process2.kill()
        self.process2.terminate()

        self.process3.kill()
        self.process3.terminate()

        self.process4.kill()
        self.process4.terminate()