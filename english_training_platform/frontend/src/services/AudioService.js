// 音频服务 - 用于跨组件管理音频播放
class AudioService {
          constructor() {
                    this.audio = null;
                    this.currentSrc = '';
                    this.isPlaying = false;
                    this.listeners = {
                              play: [],
                              pause: [],
                              ended: [],
                              timeupdate: []
                    };
          }

          // 初始化或切换音频源
          setAudioSource(src) {
                    if (this.currentSrc === src && this.audio) {
                              return this.audio;
                    }

                    // 如果之前有音频在播放，先停止并清理
                    if (this.audio) {
                              this.pause();
                              this.audio.removeEventListener('play', this._handlePlay);
                              this.audio.removeEventListener('pause', this._handlePause);
                              this.audio.removeEventListener('ended', this._handleEnded);
                              this.audio.removeEventListener('timeupdate', this._handleTimeUpdate);
                    }

                    // 创建新的音频元素
                    this.audio = new Audio(src);
                    this.currentSrc = src;

                    // 绑定事件
                    this._handlePlay = () => {
                              this.isPlaying = true;
                              this._triggerEvent('play');
                    };

                    this._handlePause = () => {
                              this.isPlaying = false;
                              this._triggerEvent('pause');
                    };

                    this._handleEnded = () => {
                              this.isPlaying = false;
                              this._triggerEvent('ended');
                    };

                    this._handleTimeUpdate = () => {
                              this._triggerEvent('timeupdate');
                    };

                    this.audio.addEventListener('play', this._handlePlay);
                    this.audio.addEventListener('pause', this._handlePause);
                    this.audio.addEventListener('ended', this._handleEnded);
                    this.audio.addEventListener('timeupdate', this._handleTimeUpdate);

                    return this.audio;
          }

          // 播放
          play() {
                    if (this.audio) {
                              return this.audio.play();
                    }
                    return Promise.reject(new Error('No audio source set'));
          }

          // 暂停
          pause() {
                    if (this.audio) {
                              this.audio.pause();
                    }
          }

          // 重置（回到开始位置）
          reset() {
                    if (this.audio) {
                              this.audio.currentTime = 0;
                    }
          }

          // 停止并完全重置（用于切换页面或离开应用时）
          stopAndReset() {
                    if (this.audio) {
                              this.pause();
                              this.reset();
                              this.isPlaying = false;
                    }
          }

          // 获取当前播放时间
          getCurrentTime() {
                    return this.audio ? this.audio.currentTime : 0;
          }

          // 获取音频总时长
          getDuration() {
                    return this.audio ? this.audio.duration : 0;
          }

          // 设置当前播放时间
          setCurrentTime(time) {
                    if (this.audio) {
                              this.audio.currentTime = time;
                    }
          }

          // 获取播放进度百分比
          getProgress() {
                    if (this.audio && this.audio.duration) {
                              return (this.audio.currentTime / this.audio.duration) * 100;
                    }
                    return 0;
          }

          // 添加事件监听器
          addEventListener(event, callback) {
                    if (this.listeners[event]) {
                              this.listeners[event].push(callback);
                    }
          }

          // 移除事件监听器
          removeEventListener(event, callback) {
                    if (this.listeners[event]) {
                              this.listeners[event] = this.listeners[event].filter(cb => cb !== callback);
                    }
          }

          // 触发事件
          _triggerEvent(event) {
                    if (this.listeners[event]) {
                              this.listeners[event].forEach(callback => callback());
                    }
          }
}

// 导出单例实例
export default new AudioService(); 