from mcelery.celery import celery_app


def register_infer_tasks():
    @celery_app.task(name="cosy_infer", queue="cosy_infer")
    def cosy_infer_task(text: str, prompt_text_cos: str, prompt_wav_cos: str, output_cos: str, mode: int = 1) -> str:
        """
        COSY TTS 服务
        :param text: 音频文字内容
        :param prompt_text_cos: 参考文本 COS key, 据说是训练 rvc 的时候放入
        :param prompt_wav_cos: 参考音频 COS key
        :param output_cos: 合成的音频文件 COS key
        :param mode: 模式： 1 中文[同语言克隆] 2 中日英混合[跨语言克隆]
        :return: output_cos
        """
        pass

    @celery_app.task(name="azure_infer", queue="azure_infer")
    def azure_infer_task(text: str, audio_profile: str, output_cos: str) -> str:
        """
        微软 TTS 服务
        :param text: 音频文字内容
        :param audio_profile: 配置
        :param output_cos: 合成的音频文件 COS key
        :return: output_cos
        """
        pass

    @celery_app.task(name="rvc_infer", queue="rvc_infer")
    def rvc_infer_task(audio_cos: str, index_cos: str, model_cos: str, pitch: int, output_cos: str) -> str:
        """
        RVC TTS 服务
        :param audio_cos: 原始音频 COS key
        :param index_cos: 模型 index COS key
        :param model_cos: 模型 weight COS key
        :param pitch: TODO
        :param output_cos: 转换后的音频 COS key
        :return: output_cos
        """
        pass

    @celery_app.task(name="srt_infer", queue="srt_infer")
    def srt_infer_task(audio_cos: str, text: str, output_cos: str) -> str:
        """
        根据音频文件生成字幕服务
        :param audio_cos: 音频文件 COS key
        :param text: 文本，原始文案，通过提供原始文案可以使asr结果更准确。请确保文案与音频内容一致
        :param output_cos: 输出的字幕文件 COS key
        :return: output_cos
        """
        pass

    @celery_app.task(name="talking_head_infer", queue="talking_head_infer")
    def talking_head_infer_task(audio_cos: str, speaker: str, output_cos: str) -> str:
        """
        根据音频生成数字人视频服务
        :param audio_cos: 音频文件
        :param speaker: 使用的数字人
        :param output_cos: 输出的视频文件 COS key
        :return: output_cos
        """
        pass

    return cosy_infer_task, azure_infer_task, rvc_infer_task, srt_infer_task, talking_head_infer_task
