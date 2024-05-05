import time
import sys

class ImgRecovery:
    def __init__(self):
        self.buffer = list()
        self.count = 0
        self.count_end = 0
        self.img_buffer = list()
        self.end_buffer = list()
        self.found_image = False
        self.img_count = 0

    def create_jpg(self):
        output = list()
        output += [0XFF, 0XD8, 0XFF, 0XE0, 0X00, 0X10, 0X4A, 0X46, 0X49, 0X46] + self.img_buffer + [0xFF, 0xD9, 0x00, 0x00]
        file = open(f"output-{self.img_count}.jpg", "wb")
        file.write(bytearray(output))
        file.close()

    def add_char(self, char):
        tmp = list()
        if self.count < 10:
            self.buffer.append(char)
            self.count += 1
            if self.count == 10:
                return True
            return False
        else:
            for i in range(0, 8):
                tmp.append(self.buffer[i+1])
            tmp.append(char)
            self.buffer = tmp
            return True
        
    def add_char_end(self, char):
        tmp = list()
        if self.count_end < 4:
            self.end_buffer.append(char)
            self.count_end += 1
            if self.count_end == 4:
                return True
            return False
        else:
            self.img_buffer.append(self.end_buffer[0])
            for i in range(0, 3):
                tmp.append(self.end_buffer[i+1])
            tmp.append(char)
            self.end_buffer = tmp
            return True
        
    def check_end(self):
        pattern = [0xFF, 0xD9, 0x00, 0x00]
        for i in range(0, 4):
            if self.end_buffer[i] != pattern[i]:
                return False
        return True
            
    def check_header(self):
        pattern = [0XFF, 0XD8, 0XFF, 0XE0, 0X00, 0X10, 0X4A, 0X46, 0X49, 0X46]; 
        pattern_reversed = [0x46, 0x49, 0x46, 0x4a, 0x10, 0x00, 0xe0, 0xff, 0xd8, 0xff]
        for i in range(0, 9):
            if self.buffer[i] != pattern[i]:
                return False
        return True
    
    def main(self):
        info_frequency = 1
        if len(sys.argv) < 2:
            print("""
            Use command: python main.py <path_to_binary_file> <info_frequency>
            - path_to_binary_file - path where your input file is located
            - info_frequency argument is optional (default 1) - inform me about progress after this amount of MBs processed
                  """)
            return
        if len(sys.argv) == 3:
            info_frequency = int(sys.argv[2])
        file = open(sys.argv[1], "rb")
        content = file.read()
        file.close()
        length = len(content)
        cur_index = -1
        start = time.time()
        content = content + bytes([0x0, 0x0])
        for char in content:
            cur_index += 1
            if cur_index % (1024 * 1024 * info_frequency) == 0:
                print("progress: " + str(int((cur_index / (1024 * 1024 * info_frequency)) / (length / (1024 * 1024 * info_frequency)) * 100)) + "%")
            if not self.found_image:
                if self.add_char(char):
                    if self.check_header():
                        print("found image start")
                        self.found_image = True
            else:
                if self.add_char_end(char):
                    if self.check_end():
                        print("found image end")
                        self.create_jpg()
                        self.found_image = False
                        self.img_count += 1
                        self.buffer = list()
                        self.end_buffer = list()
                        self.img_buffer = list()
                        self.count = 0
                        self.count_end = 0
        print("progress: 100%")
        endtime = time.time()
        result_time = endtime - start
        flow = length / result_time
        print(f"{str(flow)} byte/s")
        return

a = ImgRecovery()
a.main()
