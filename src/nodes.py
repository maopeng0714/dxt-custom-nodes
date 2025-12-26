from .cloud.aliyun_oss_uploader import *
from .remote_flux1 import RemoteFlux1Generator

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique

NODE_CLASS_MAPPINGS = {
    "AliyunOSSImageUploader": AliyunOSSImageUploader,
    "AliyunOSSVideoUploader": AliyunOSSVideoUploader,
    "AliyunOSSAudioUploader": AliyunOSSAudioUploader,
    "RemoteFlux1Generator": RemoteFlux1Generator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AliyunOSSImageUploader": "阿里云OSS图片上传",
    "AliyunOSSVideoUploader": "阿里云OSS视频上传",
    "AliyunOSSAudioUploader": "阿里云OSS音频上传",
    "RemoteFlux1Generator": "远程Flux1图像生成"
}
