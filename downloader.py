import os
import json
import re
import platform
import shutil
import subprocess
import sys
import yt_dlp

def is_android() -> bool:
    """Yalnız həqiqi Android mühitini təyin edir. 
    Linux sistemində 'getandroidapilevel' və ya 'ANDROID_DATA' olmadığından həmişə False qaytaracaq."""
    return hasattr(sys, "getandroidapilevel") or "ANDROID_DATA" in os.environ


class Settings:
    def __init__(self, app_path: str):
        self.app_path = app_path
        self.settings_file = os.path.join(app_path, "settings.json")
        self.data = {
            "lang": "en",
            "theme": "dark",
            "positions": {},
            "qualities": {}
        }
        self._load()

    def _load(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    if isinstance(loaded, dict):
                        self.data.update(loaded)
            except Exception:
                pass

    def _save(self):
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    @property
    def lang(s) -> str:
        return s.data.get("lang", "en")

    @lang.setter
    def lang(s, value: str):
        s.data["lang"] = value
        s._save()

    @property
    def theme(s) -> str:
        return s.data.get("theme", "dark")

    @theme.setter
    def theme(s, value: str):
        s.data["theme"] = value
        s._save()

    def get_position(self, filename: str) -> int:
        return self.data.get("positions", {}).get(filename, 0)

    def set_position(self, filename: str, pos: int):
        if "positions" not in self.data:
            self.data["positions"] = {}
        self.data["positions"][filename] = pos
        self._save()

    def get_quality(self, filename: str) -> str:
        return self.data.get("qualities", {}).get(filename, "—")

    def set_quality(self, filename: str, quality: str):
        if "qualities" not in self.data:
            self.data["qualities"] = {}
        self.data["qualities"][filename] = quality
        self._save()

    def remove_video_meta(self, filename: str):
        updated = False
        if "positions" in self.data and filename in self.data["positions"]:
            del self.data["positions"][filename]
            updated = True
        if "qualities" in self.data and filename in self.data["qualities"]:
            del self.data["qualities"][filename]
            updated = True
        if updated:
            self._save()


class Downloader:
    def __init__(self, app_path: str):
        self.base_dir = app_path
        os.makedirs(self.base_dir, exist_ok=True)
        self.is_cancelled = False
        
        print(f"[LOG] [Downloader] Başladılır. Əsas qovluq: {self.base_dir}")
        self.ffmpeg_dir = self._ffmpeg_path_scan()
        self._verify_binaries()

        self.name = ""
        self.mb = "—"
        self.speed = "—"
        self.percent = "0%"
        self.quality = "—"

    def cancel(self):
        self.is_cancelled = True
        print("[LOG] [Downloader] LƏĞV EDİLDİ: İstifadəçi yükləməni dayandırdı.")

    def _detect_abi(self) -> str:
        """Bir neçə mənbədən arxitekturanı yoxlayır (platform.machine() tək başına
        bəzi Android qurğularında/tərcümə qatlarında yanlış nəticə verə bilər)."""
        candidates = []

        try:
            candidates.append(platform.machine())
        except Exception:
            pass

        try:
            candidates.append(os.uname().machine)
        except Exception:
            pass

        try:
            result = subprocess.run(
                ["uname", "-m"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                candidates.append(result.stdout.strip())
        except Exception:
            pass

        env_arch = os.environ.get("ANDROID_ARCH") or os.environ.get("ARCH")
        if env_arch:
            candidates.append(env_arch)

        print(f"[Arch Detect] Toplanan namizədlər: {candidates}")

        for c in candidates:
            c_low = c.lower()
            if "aarch64" in c_low or "arm64" in c_low:
                print(f"[Arch Detect] '{c}' -> arm64-v8a")
                return "arm64-v8a"
            if "armv7" in c_low or "armeabi" in c_low or ("arm" in c_low and "64" not in c_low):
                print(f"[Arch Detect] '{c}' -> armeabi-v7a")
                return "armeabi-v7a"

        print("[WARNING] [Arch Detect] Heç bir namizəd tanınmadı, defolt olaraq arm64-v8a seçilir")
        return "arm64-v8a"

    def _ffmpeg_path_scan(self) -> str:
        android_status = is_android()
        print(f"[FFmpeg Scan] Android mühiti: {android_status}")
        
        binaries = ("ffmpeg", "ffprobe")
        
        if android_status:
            abi = self._detect_abi()
            print(f"[FFmpeg Scan] Android ABI təyin edildi: {abi}")
            
            target_bin_dir = os.path.join(self.base_dir, "bin")
            os.makedirs(target_bin_dir, exist_ok=True)
            
            base_path = os.path.dirname(os.path.abspath(__file__))
            assets_env = os.environ.get("FLET_ASSETS_DIR")
            
            possible_source_dirs = [
                os.path.join(assets_env, "ffmpeg", abi) if assets_env else "",
                os.path.join(base_path, "assets", "ffmpeg", abi),
                os.path.join(base_path, "ffmpeg", abi),
                os.path.join(os.path.dirname(base_path), "assets", "ffmpeg", abi),
                os.path.join(os.path.dirname(os.path.dirname(base_path)), "assets", "ffmpeg", abi)
            ]
            
            source_dir = None
            for d in possible_source_dirs:
                if d and os.path.exists(d):
                    if os.path.exists(os.path.join(d, "ffmpeg")):
                        source_dir = d
                        break
            
            for bin_name in binaries:
                target_file = os.path.join(target_bin_dir, bin_name)
                
                if not os.path.exists(target_file) and source_dir:
                    source_file = os.path.join(source_dir, bin_name)
                    if os.path.exists(source_file):
                        try:
                            shutil.copy(source_file, target_file)
                            print(f"[OK] [{bin_name}] Daxili yaddaşa kopyalandı")
                        except Exception as ex:
                            print(f"[ERROR] [{bin_name}] Kopyalama xətası: {ex}")
                
                if os.path.exists(target_file):
                    try:
                        os.chmod(target_file, 0o755)
                    except Exception:
                        pass
            
            if os.path.exists(os.path.join(target_bin_dir, "ffmpeg")):
                return target_bin_dir
            return None

        else:
            print("[LOG] [FFmpeg] Linux/Desktop mühitidir. Sistemdəki (PATH) ffmpeg istifadə ediləcək.")
            return None

    def _run_version_check(self, exe_path: str, label: str):
        try:
            result = subprocess.run(
                [exe_path, "-version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                first_line = result.stdout.splitlines()[0] if result.stdout else "(boş output)"
                print(f"[OK] [{label}] -version uğurlu: {first_line}")
            else:
                print(f"[ERROR] [{label}] -version xəta kodu {result.returncode}: {result.stderr.strip()}")
        except FileNotFoundError:
            print(f"[ERROR] [{label}] Binar tapılmadı: {exe_path}")
        except PermissionError:
            print(f"[ERROR] [{label}] İcazə xətası (chmod +x yoxla): {exe_path}")
        except subprocess.TimeoutExpired:
            print(f"[ERROR] [{label}] -version çağırışı vaxtı bitdi: {exe_path}")
        except Exception as ex:
            print(f"[ERROR] [{label}] Naməlum xəta: {ex}")

    def _verify_binaries(self):
        android_status = is_android()
        for bin_name in ("ffmpeg", "ffprobe"):
            if self.ffmpeg_dir:
                exe_path = os.path.join(self.ffmpeg_dir, bin_name)
            elif android_status:
                print(f"[ERROR] [{bin_name}] Android üçün binar qovluğu tapılmadı, yoxlama edilmir")
                continue
            else:
                exe_path = shutil.which(bin_name) or bin_name

            self._run_version_check(exe_path, bin_name)

    def probe_qualities(self, url: str) -> list:
        print(f"[LOG] [Probe] Keyfiyyətlər yoxlanılır. URL: {url}")
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "nocheckcertificate": True,
        }
        if self.ffmpeg_dir:
            ydl_opts["ffmpeg_location"] = self.ffmpeg_dir

        heights = []
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                seen = set()
                for f in formats:
                    h = f.get('height')
                    if h and h not in seen:
                        seen.add(h)
                        heights.append(h)
                heights = sorted(list(seen), reverse=True)
                print(f"[OK] [Probe] Tapılan keyfiyyətlər: {heights}")
        except Exception as e:
            print(f"[ERROR] [Probe Error]: {e}")
        return heights

    def _progress_hook(self, d):
        if self.is_cancelled:
            raise Exception("Download cancelled by user")

        if d['status'] == 'downloading':
            self.name = d.get('info_dict', {}).get('title', 'Video')
            
            p_str = d.get('_percent_str', '0%').strip()
            p_str = re.sub(r'\x1b\[[0-9;]*m', '', p_str)
            self.percent = p_str if p_str else '0%'
            
            s_str = d.get('_speed_str', '—').strip()
            s_str = re.sub(r'\x1b\[[0-9;]*m', '', s_str)
            self.speed = s_str if s_str else '—'
            
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            if total > 0:
                self.mb = f"{downloaded / 1024 / 1024:.1f} / {total / 1024 / 1024:.1f} MB"
            else:
                self.mb = f"{downloaded / 1024 / 1024:.1f} MB"
                
        elif d['status'] == 'finished':
            self.percent = '100%'
            self.mb = 'Tamamlandı'

    def download(self, url: str, quality: str = "best"):
        self.is_cancelled = False
        self.name = "Başlayır..."
        self.percent = "0%"
        self.speed = "—"
        self.mb = "—"

        if quality == "best":
            fmt = "bestvideo[height<=1440][protocol=https]+bestaudio[protocol=https]/best[protocol=https]"
            actual_quality = "Auto"
        else:
            fmt = f"bestvideo[height<={quality}][protocol=https]+bestaudio[protocol=https]/best[height<={quality}][protocol=https]/best"
            actual_quality = f"{quality}p"

        self.quality = actual_quality

        ydl_opts = {
            "format": fmt,
            "merge_output_format": "mp4",
            "outtmpl": os.path.join(self.base_dir, "%(title)s.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
            "nocheckcertificate": True,
            "retries": 10,
            "fragment_retries": 10,
            "concurrent_fragment_downloads": 4,
            "progress_hooks": [self._progress_hook],
            "writethumbnail": True,
            "postprocessors": [{"key": "FFmpegThumbnailsConvertor", "format": "jpg"}],
        }

        if self.ffmpeg_dir:
            ydl_opts["ffmpeg_location"] = self.ffmpeg_dir

        final_filename = None
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if 'filepath' in info:
                    final_filename = os.path.basename(info['filepath'])
                else:
                    filename = os.path.basename(ydl.prepare_filename(info))
                    base, _ = os.path.splitext(filename)
                    final_filename = base + ".mp4"
                
                if not os.path.exists(os.path.join(self.base_dir, final_filename)):
                    files = self.list_videos()
                    if files:
                        final_filename = files[0]
        except Exception as e:
            err_msg = str(e)
            self.name = "Xəta baş verdi"
            self.percent = "Xəta"
            self.speed = "—"
            self.mb = err_msg[:30] + "..." if len(err_msg) > 30 else err_msg
            raise e

        return final_filename, actual_quality

    def list_videos(self):
        if not os.path.exists(self.base_dir):
            return []
        valid_exts = ('.mp4', '.mkv', '.webm', '.mov', '.avi')
        files = []
        for f in os.listdir(self.base_dir):
            if f.lower().endswith(valid_exts):
                files.append(f)
        return sorted(files, key=lambda x: os.path.getmtime(os.path.join(self.base_dir, x)), reverse=True)

    def video_path(self, filename: str) -> str:
        return os.path.join(self.base_dir, filename)

    def thumb_path(self, filename: str):
        base_name, _ = os.path.splitext(filename)
        for ext in ('.jpg', '.webp', '.png'):
            thumb_file = os.path.join(self.base_dir, base_name + ext)
            if os.path.exists(thumb_file):
                return thumb_file
        return None

    def delete_video(self, filename: str):
        v_path = self.video_path(filename)
        if os.path.exists(v_path):
            os.remove(v_path)
        base_name, _ = os.path.splitext(filename)
        for ext in ('.jpg', '.webp', '.png'):
            thumb_file = os.path.join(self.base_dir, base_name + ext)
            if os.path.exists(thumb_file):
                os.remove(thumb_file)
