from subprocess import check_output, STDOUT, CalledProcessError

class EncDec:
    def __init__(self, key_encrypt, kid_encrypt, schema_encrypt):
        self.key_encrypt = key_encrypt
        self.kid_encrypt = kid_encrypt
        self.schema_encrypt = schema_encrypt

    def encrypt_video(self, path_input_video, path_output_video):
      ffmpeg_command = ['ffmpeg', 
                  '-i', path_input_video, 
                  "-vcodec", "copy",
                  "-encryption_scheme", self.schema_encrypt, 
                  "-encryption_key", self.key_encrypt,
                  "-encryption_kid", self.kid_encrypt, path_output_video]
      try:
          output_ffmpeg_execution = check_output(ffmpeg_command, stderr=STDOUT)
          print(output_ffmpeg_execution)
      except CalledProcessError as e:
          raise e

    def decrypt_video(self, path_input_video, path_output_video):
        ffmpeg_command = ['ffmpeg', 
            "-decryption_key", self.key_encrypt,
            '-i', path_input_video, 
            '-vcodec', 'copy', path_output_video]

        try:
            output_ffmpeg_execution = check_output(ffmpeg_command, stderr=STDOUT)
            print(output_ffmpeg_execution)
        except CalledProcessError as e:
            raise e

# if __name__ == "__main__":
#     key_encrypt = "54da3a085bb24aa4889e99712867880d"
#     kid_encrypt = "2522b17ecc28451a89d9e733445a6064"
#     schema_encrypt = "cenc-aes-ctr"
#     encdec = EncDec(key_encrypt=key_encrypt, kid_encrypt=kid_encrypt, schema_encrypt=schema_encrypt)
#     encdec.encrypt_video("./video.mp4", "./video_encrypted.mp4")
#     encdec.decrypt_video("./video_encrypted.mp4", "./video_decrypted.mp4")