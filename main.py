import asyncio
import os
import traceback

import flet as ft
import flet_video as ftv
from downloader import Downloader, Settings


def get_app_path():
    if "ANDROID_DATA" in os.environ or "ANDROID_ROOT" in os.environ:
        return os.environ.get("HOME", os.getcwd())
    return os.getcwd()


PRIMARY = "#FF0000"
PRIMARY_LIGHT = "#FFE3E3"

THEMES = {
    "dark": {
        "bg": "#121212",
        "card_bg": "#1E1E1E",
        "text_main": "#FFFFFF",
        "text_sub": "#AAAAAA",
        "border": "#2A2A2A",
    },
    "light": {
        "bg": "#F9F9F9",
        "card_bg": "#FFFFFF",
        "text_main": "#0F0F0F",
        "text_sub": "#606060",
        "border": "#E0E0E0",
    },
}

QUALITY_OPTIONS = [
    ("best", "Auto (Ən yüksək)"),
    ("2160", "2160p (4K)"),
    ("1440", "1440p (2K)"),
    ("1080", "1080p"),
    ("720", "720p"),
    ("480", "480p"),
    ("360", "360p"),
]

LANGUAGES = [
    ("en", "English"),
    ("az", "Azərbaycan"),
    ("tr", "Türkçe"),
    ("ru", "Русский"),
    ("ar", "العربية"),
    ("es", "Español"),
    ("fr", "Français"),
    ("de", "Deutsch"),
    ("pt", "Português"),
]

TRANSLATIONS = {
    "en": {
        "app_title": "TStube",
        "library": "Library",
        "download": "Download",
        "cancel": "Cancel",
        "no_videos": "No videos yet",
        "url_label": "Video URL",
        "waiting": "Waiting",
        "starting": "Starting...",
        "downloading": "Downloading",
        "completed": "Completed",
        "error": "Error",
        "cancelled": "Cancelled",
        "err_empty_url": "Please enter a video URL",
        "err_invalid_url": "Invalid or unsupported video link",
        "err_network": "Network error — check your connection",
        "err_unavailable": "This video is unavailable or private",
        "err_storage": "Not enough storage space",
        "err_generic": "Something went wrong",
        "quality": "Quality",
    },
    "az": {
        "app_title": "TStube",
        "library": "Kitabxana",
        "download": "Yüklə",
        "cancel": "Ləğv et",
        "no_videos": "Hələ video yoxdur",
        "url_label": "Video URL",
        "waiting": "Gözləyir",
        "starting": "Başlayır...",
        "downloading": "Yüklənir",
        "completed": "Tamamlandı",
        "error": "Xəta",
        "cancelled": "Ləğv edildi",
        "err_empty_url": "Zəhmət olmasa video linki daxil edin",
        "err_invalid_url": "Yanlış və ya dəstəklənməyən video linki",
        "err_network": "Şəbəkə xətası — internet bağlantınızı yoxlayın",
        "err_unavailable": "Bu video əlçatan deyil və ya məxfidir",
        "err_storage": "Kifayət qədər yaddaş yoxdur",
        "err_generic": "Nəsə səhv getdi",
        "quality": "Keyfiyyət",
    },
    "tr": {
        "app_title": "TStube",
        "library": "Kitaplık",
        "download": "İndir",
        "cancel": "İptal",
        "no_videos": "Henüz video yok",
        "url_label": "Video URL",
        "waiting": "Bekliyor",
        "starting": "Başlıyor...",
        "downloading": "İndiriliyor",
        "completed": "Tamamlandı",
        "error": "Hata",
        "cancelled": "İptal edildi",
        "err_empty_url": "Lütfen bir video bağlantısı girin",
        "err_invalid_url": "Geçersiz veya desteklenmeyen video bağlantısı",
        "err_network": "Ağ hatası — internet bağlantınızı kontrol edin",
        "err_unavailable": "Bu video kullanılamıyor veya gizli",
        "err_storage": "Yeterli depolama alanı yok",
        "err_generic": "Bir şeyler ters gitti",
        "quality": "Kalite",
    },
    "ru": {
        "app_title": "TStube",
        "library": "Библиотека",
        "download": "Скачать",
        "cancel": "Отмена",
        "no_videos": "Пока нет видео",
        "url_label": "Ссылка на видео",
        "waiting": "Ожидание",
        "starting": "Запуск...",
        "downloading": "Загрузка",
        "completed": "Завершено",
        "error": "Ошибка",
        "cancelled": "Отменено",
        "err_empty_url": "Пожалуйста, введите ссылку на видео",
        "err_invalid_url": "Неверная или неподдерживаемая ссылка на видео",
        "err_network": "Ошибка сети — проверьте подключение",
        "err_unavailable": "Видео недоступно или является приватным",
        "err_storage": "Недостаточно места для хранения",
        "err_generic": "Что-то пошло не так",
        "quality": "Качество",
    },
    "ar": {
        "app_title": "TStube",
        "library": "المكتبة",
        "download": "تنزيل",
        "cancel": "إلغاء",
        "no_videos": "لا توجد مقاطع فيديو بعد",
        "url_label": "رابط الفيديو",
        "waiting": "في الانتظار",
        "starting": "جارٍ البدء...",
        "downloading": "جارٍ التنزيل",
        "completed": "اكتمل",
        "error": "خطأ",
        "cancelled": "تم الإلغاء",
        "err_empty_url": "الرجاء إدخال رابط الفيديو",
        "err_invalid_url": "رابط فيديو غير صالح أو غير مدعوم",
        "err_network": "خطأ في الشبكة — تحقق من اتصالك",
        "err_unavailable": "هذا الفيديو غير متاح أو خاص",
        "err_storage": "لا توجد مساحة تخزين كافية",
        "err_generic": "حدث خطأ ما",
        "quality": "الجودة",
    },
    "es": {
        "app_title": "TStube",
        "library": "Biblioteca",
        "download": "Descargar",
        "cancel": "Cancelar",
        "no_videos": "Aún no hay videos",
        "url_label": "URL del video",
        "waiting": "Esperando",
        "starting": "Iniciando...",
        "downloading": "Descargando",
        "completed": "Completado",
        "error": "Error",
        "cancelled": "Cancelado",
        "err_empty_url": "Por favor, introduce un enlace de video",
        "err_invalid_url": "En enlace de video inválido o no compatible",
        "err_network": "Error de red — revisa tu conexión",
        "err_unavailable": "Este video no está disponible o es privado",
        "err_storage": "No hay suficiente espacio de almacenamiento",
        "err_generic": "Algo salió mal",
        "quality": "Calidad",
    },
    "fr": {
        "app_title": "TStube",
        "library": "Bibliothèque",
        "download": "Télécharger",
        "cancel": "Annuler",
        "no_videos": "Aucune vidéo pour le moment",
        "url_label": "URL de la vidéo",
        "waiting": "En attente",
        "starting": "Démarrage...",
        "downloading": "Téléchargement",
        "completed": "Terminé",
        "error": "Erreur",
        "cancelled": "Annulé",
        "err_empty_url": "Veuillez saisir un lien vidéo",
        "err_invalid_url": "Lien vidéo invalide ou non pris en charge",
        "err_network": "Erreur réseau — vérifiez votre connexion",
        "err_unavailable": "Cette vidéo est indisponible ou privée",
        "err_storage": "Espace de stockage insuffisant",
        "err_generic": "Un problème est survenu",
        "quality": "Qualité",
    },
    "de": {
        "app_title": "TStube",
        "library": "Bibliothek",
        "download": "Herunterladen",
        "cancel": "Abbrechen",
        "no_videos": "Noch keine Videos",
        "url_label": "Video-URL",
        "waiting": "Wartet",
        "starting": "Startet...",
        "downloading": "Wird heruntergeladen",
        "completed": "Abgeschlossen",
        "error": "Fehler",
        "cancelled": "Abgebrochen",
        "err_empty_url": "Bitte einen Video-Link eingeben",
        "err_invalid_url": "Ungültiger oder nicht unterstützter Video-Link",
        "err_network": "Netzwerkfehler — Verbindung prüfen",
        "err_unavailable": "Dieses Video ist nicht verfügbar oder privat",
        "err_storage": "Nicht genügend Speicherplatz",
        "err_generic": "Etwas ist schiefgelaufen",
        "quality": "Qualität",
    },
    "pt": {
        "app_title": "TStube",
        "library": "Biblioteca",
        "download": "Baixar",
        "cancel": "Cancelar",
        "no_videos": "Ainda não há vídeos",
        "url_label": "URL do vídeo",
        "waiting": "Aguardando",
        "starting": "Iniciando...",
        "downloading": "Baixando",
        "completed": "Concluído",
        "error": "Erro",
        "cancelled": "Cancelado",
        "err_empty_url": "Por favor, insira um link de vídeo",
        "err_invalid_url": "Link de vídeo inválido ou não suportado",
        "err_network": "Erro de rede — verifique sua conexão",
        "err_unavailable": "Este vídeo está indisponible ou é privado",
        "err_storage": "Espaço de armazenamento insuficiente",
        "err_generic": "Algo deu errado",
        "quality": "Qualidade",
    },
}


def main(page: ft.Page):
    page.title = "TStube"
    page.padding = 0

    app_path = get_app_path()
    dl = Downloader(app_path=app_path)
    settings = Settings(app_path)

    state = {
        "lang": settings.lang if settings.lang in TRANSLATIONS else "en",
        "theme": settings.theme if settings.theme in THEMES else "dark",
    }

    # Hazırda açıq olan video player üçün geri naviqasiya callback-i.
    current_player_back = {"callback": None}

    async def handle_view_pop(e):
        # Android Back düyməsi/gesture və View back hadisəsi burada tutulur.
        callback = current_player_back.get("callback")
        if callback:
            await callback()
            return

        # Player yoxdursa, normal view pop davranışı.
        if e.view is not None and e.view in page.views and len(page.views) > 1:
            page.views.remove(e.view)
            page.update()

    page.on_view_pop = handle_view_pop

    def get_colors():
        return THEMES[state["theme"]]

    def t(key):
        return TRANSLATIONS.get(state["lang"], TRANSLATIONS["en"]).get(key, key)

    page.rtl = state["lang"] == "ar"

    def show_error(message: str):
        try:
            page.show_dialog(
                ft.SnackBar(content=ft.Text(message), bgcolor=ft.Colors.RED_400)
            )
        except Exception:
            traceback.print_exc()

    video_list = ft.ListView(expand=True, spacing=10, padding=14)

    current_player = {"back": None}

    def handle_view_pop(e):
        callback = current_player.get("back")
        if callback:
            callback()
        elif len(page.views) > 1:
            page.views.pop()
            page.update()

    page.on_view_pop = handle_view_pop

    def open_video(filename):
        def go(e):
            try:
                colors = get_colors()

                # Playback vəziyyəti:
                # pos -> son məlum mövqe (millisaniyə)
                # active -> player hələ açıqdırmı
                # last_saved -> diskə son yazılan vaxt
                track = {
                    "active": True,
                    "pos": 0,
                    "last_saved": 0.0,
                    "resume_started": False,
                }

                # Əvvəlki sessiyadan saxlanmış mövqeni oxu.
                try:
                    track["pos"] = max(0, int(settings.get_position(filename) or 0))
                except Exception:
                    track["pos"] = 0

                def save_position(force=False):
                    """Mövqeni Settings vasitəsilə qalıcı yadda saxla."""
                    try:
                        import time

                        now = time.monotonic()

                        # Position dəyişiklikləri çox tez-tez gəlirsə diskə
                        # hər event-də yazmaq əvəzinə təxminən saniyədə 1 dəfə yaz.
                        if not force and (now - track["last_saved"]) < 1.0:
                            return

                        settings.set_position(filename, max(0, int(track["pos"])))
                        track["last_saved"] = now
                    except Exception:
                        traceback.print_exc()

                async def resume_position():
                    """
                    Video native Android player tərəfindən hazır olduqdan sonra
                    saxlanmış mövqeyə keçməyə çalışır.

                    Android-də player-in ilk anda seek qəbul etməməsi mümkündür,
                    buna görə bir neçə dəfə, aralıqla yoxlanılır.
                    """
                    if track["resume_started"]:
                        return

                    track["resume_started"] = True
                    saved_pos = max(0, int(track["pos"]))

                    # 0 və ya çox kiçik mövqe üçün seek lazım deyil.
                    if saved_pos < 1500:
                        return

                    # Native player-in hazırlanması üçün gözlə.
                    for delay in (0.8, 1.2, 1.5):
                        if not track["active"]:
                            return

                        await asyncio.sleep(delay)

                        if not track["active"]:
                            return

                        try:
                            seek_method = getattr(video_ctrl, "seek", None)
                            if seek_method is None:
                                return

                            result = seek_method(saved_pos)

                            # Flet/Flet Video versiyasına görə seek coroutine
                            # və ya adi method ola bilər.
                            if hasattr(result, "__await__"):
                                await result

                            print(
                                f"[PLAYER] Resume: {filename} -> "
                                f"{saved_pos} ms"
                            )
                            return

                        except Exception as ex:
                            print(
                                f"[PLAYER] Resume seek failed: {ex}"
                            )

                    # Seek alınmasa belə mövqe yaddaşda qalır; növbəti açılışda
                    # yenidən cəhd ediləcək.
                    print(
                        f"[PLAYER] Resume failed, saved position kept: "
                        f"{saved_pos} ms"
                    )

                def go_back(ev=None):
                    if not track["active"]:
                        return

                    # Əvvəl mövqeni yadda saxla, sonra player-i bağla.
                    save_position(force=True)

                    track["active"] = False
                    current_player["back"] = None

                    if len(page.views) > 1:
                        page.views.pop()
                        page.update()

                current_player["back"] = go_back

                def on_position_change(ev):
                    if not track["active"]:
                        return

                    try:
                        data = getattr(ev, "data", None)

                        if hasattr(data, "in_milliseconds"):
                            position = int(data.in_milliseconds)
                        elif isinstance(data, (int, float)):
                            position = int(data)
                        elif isinstance(data, str):
                            position = int(float(data))
                        else:
                            return

                        if position >= 0:
                            track["pos"] = position

                            # Son mövqeni davamlı olaraq qalıcı yadda saxla.
                            # Beləliklə app qəfil bağlansa/kəsilsə belə son
                            # saxlanmış mövqe mümkün qədər aktual qalır.
                            save_position()

                    except Exception:
                        pass

                video_ctrl = ftv.Video(
                    playlist=[ftv.VideoMedia(dl.video_path(filename))],
                    autoplay=True,
                    expand=True,
                    on_position_change=on_position_change,
                    controls=ftv.AdaptiveVideoControls(
                        material=ftv.MaterialVideoControls(
                            visible_on_mount=True,
                            display_seek_bar=True,
                            seek_gesture=True,
                            seek_on_double_tap=True,
                            seek_on_double_tap_backward_duration=10000,
                            seek_on_double_tap_forward_duration=10000,
                            volume_gesture=True,
                            brightness_gesture=True,
                            speed_up_on_long_press=True,
                            speed_up_factor=2.5,
                        ),
                        material_desktop=ftv.MaterialDesktopVideoControls(
                            visible_on_mount=True,
                            display_seek_bar=True,
                        ),
                    ),
                )

                page.views.append(
                    ft.View(
                        route="/player",
                        padding=0,
                        bgcolor=colors["bg"],
                        controls=[
                            ft.SafeArea(
                                content=ft.Column(
                                    [
                                        ft.AppBar(
                                            title=ft.Text(
                                                "TStube",
                                                size=16,
                                                color=ft.Colors.WHITE,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            bgcolor=ft.Colors.BLACK,
                                            leading=ft.IconButton(
                                                icon=ft.Icons.ARROW_BACK,
                                                icon_color=ft.Colors.WHITE,
                                                on_click=go_back,
                                            ),
                                        ),
                                        ft.Container(
                                            content=video_ctrl,
                                            bgcolor=ft.Colors.BLACK,
                                            aspect_ratio=16 / 9,
                                        ),
                                        ft.Container(
                                            expand=True,
                                            padding=16,
                                            content=ft.Column(
                                                [
                                                    ft.Text(
                                                        os.path.splitext(
                                                            filename
                                                        )[0],
                                                        size=16,
                                                        weight=ft.FontWeight.W_600,
                                                        color=colors[
                                                            "text_main"
                                                        ],
                                                        max_lines=2,
                                                        overflow=ft.TextOverflow.ELLIPSIS,
                                                    ),
                                                    ft.Row(
                                                        [
                                                            ft.Container(
                                                                content=ft.Icon(
                                                                    ft.Icons.PLAY_ARROW_ROUNDED,
                                                                    size=14,
                                                                    color=ft.Colors.WHITE,
                                                                ),
                                                                width=26,
                                                                height=26,
                                                                bgcolor=PRIMARY,
                                                                border_radius=13,
                                                                alignment=ft.Alignment.CENTER,
                                                            ),
                                                            ft.Text(
                                                                "TStube",
                                                                size=13,
                                                                color=colors[
                                                                    "text_sub"
                                                                ],
                                                            ),
                                                        ],
                                                        spacing=8,
                                                    ),
                                                ],
                                                spacing=10,
                                            ),
                                        ),
                                    ],
                                    spacing=0,
                                ),
                                expand=True,
                            )
                        ],
                    )
                )

                page.update()

                # Player artıq UI-yə əlavə edildikdən sonra saxlanmış mövqeyə
                # avtomatik qayıt.
                page.run_task(resume_position)

            except Exception:
                traceback.print_exc()
                current_player["back"] = None
                show_error(t("err_generic"))

        return go

    def delete_video(filename):
        def go(e):
            try:
                dl.delete_video(filename)
                settings.remove_video_meta(filename)
                refresh_library()
            except Exception:
                traceback.print_exc()
                show_error(t("err_generic"))

        return go

    no_videos_placeholder = ft.Container(
        padding=40,
        content=ft.Column(
            [
                ft.Icon(
                    ft.Icons.VIDEO_LIBRARY_OUTLINED,
                    size=48,
                    color=ft.Colors.GREY_500,
                ),
                ft.Text(t("no_videos"), color=ft.Colors.GREY_500),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
        ),
    )

    def refresh_library():
        colors = get_colors()
        video_list.controls.clear()
        files = dl.list_videos()
        if not files:
            no_videos_placeholder.content.controls[1].value = t("no_videos")
            video_list.controls.append(no_videos_placeholder)
        for f in files:
            thumb = dl.thumb_path(f)
            quality_label = settings.get_quality(f)

            thumb_inner = ft.Image(
                src=thumb, fit=ft.BoxFit.COVER, expand=True
            ) if thumb else ft.Icon(
                ft.Icons.PLAY_CIRCLE_FILL,
                size=48,
                color=ft.Colors.WHITE,
            )

            thumb_stack_children = [thumb_inner]
            if quality_label:
                thumb_stack_children.append(
                    ft.Container(
                        content=ft.Text(
                            quality_label,
                            size=11,
                            weight=ft.FontWeight.W_700,
                            color=ft.Colors.WHITE,
                        ),
                        bgcolor=ft.Colors.BLACK_54,
                        border_radius=6,
                        padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                        right=6,
                        bottom=6,
                    )
                )

            video_list.controls.append(
                ft.Container(
                    bgcolor=colors["card_bg"],
                    border_radius=14,
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK_12),
                    content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Stack(thumb_stack_children),
                                bgcolor="#202020" if not thumb else None,
                                alignment=ft.Alignment.CENTER,
                                aspect_ratio=16 / 9,
                                on_click=open_video(f),
                            ),
                            ft.Container(
                                padding=ft.Padding.symmetric(
                                    horizontal=10, vertical=8
                                ),
                                content=ft.Row(
                                    [
                                        ft.Container(
                                            content=ft.Icon(
                                                ft.Icons.PLAY_ARROW_ROUNDED,
                                                size=16,
                                                color=ft.Colors.WHITE,
                                            ),
                                            width=32,
                                            height=32,
                                            bgcolor=PRIMARY,
                                            border_radius=16,
                                            alignment=ft.Alignment.CENTER,
                                        ),
                                        ft.Container(
                                            content=ft.Column(
                                                [
                                                    ft.Text(
                                                        os.path.splitext(f)[0],
                                                        max_lines=2,
                                                        overflow=ft.TextOverflow.ELLIPSIS,
                                                        weight=ft.FontWeight.W_600,
                                                        size=14,
                                                        color=colors["text_main"],
                                                    ),
                                                    ft.Text(
                                                        quality_label if quality_label else "—",
                                                        size=12,
                                                        color=colors["text_sub"],
                                                    ),
                                                ],
                                                spacing=2,
                                                tight=True,
                                            ),
                                            expand=True,
                                            on_click=open_video(f),
                                        ),
                                        ft.IconButton(
                                            ft.Icons.DELETE_OUTLINE,
                                            icon_color=colors["text_sub"],
                                            on_click=delete_video(f),
                                        ),
                                    ],
                                    spacing=10,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            ),
                        ],
                        spacing=0,
                    ),
                )
            )
        page.update()

    home_view = ft.Column([video_list], expand=True)

    url_field = ft.TextField(
        label=t("url_label"),
        expand=True,
        border_radius=12,
        prefix_icon=ft.Icons.LINK,
    )
    download_btn = ft.Button(
        t("download"),
        icon=ft.Icons.DOWNLOAD,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
    )

    name_text = ft.Text(
        "", weight=ft.FontWeight.W_600, size=15, selectable=True
    )
    mb_text = ft.Text("—", size=13)
    speed_text = ft.Text("—", size=13)
    percent_text = ft.Text(
        "0%", size=22, weight=ft.FontWeight.BOLD, color=PRIMARY
    )
    progress_ring = ft.ProgressRing(
        value=0,
        width=64,
        height=64,
        color=PRIMARY,
        stroke_width=6,
        bgcolor=PRIMARY_LIGHT,
    )
    progress_bar = ft.ProgressBar(
        value=0, color=PRIMARY, bgcolor=ft.Colors.GREY_200, border_radius=8
    )
    status_chip = ft.Container(
        content=ft.Text(
            t("waiting"),
            size=12,
            color=ft.Colors.GREY_700,
            weight=ft.FontWeight.W_600,
        ),
        bgcolor=ft.Colors.GREY_200,
        border_radius=20,
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
    )

    downloading = {"active": False}

    def cancel_download_action(e):
        print("[LOG] [UI] İstifadəçi 'Ləğv et' düyməsinə basdı.")
        dl.cancel()
        status_chip.content.value = t("cancelled")
        status_chip.bgcolor = ft.Colors.ORANGE_100
        status_chip.content.color = ft.Colors.ORANGE_800
        speed_text.value = "Ləğv edildi"
        download_btn.disabled = False
        page.update()

    cancel_btn = ft.IconButton(
        icon=ft.Icons.CLOSE_ROUNDED,
        icon_color=ft.Colors.RED_400,
        tooltip="Ləğv et",
        on_click=cancel_download_action,
    )

    progress_card = ft.Container(
        border_radius=16,
        padding=18,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK_12),
        visible=False,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Stack(
                            [
                                progress_ring,
                                ft.Container(
                                    content=percent_text,
                                    alignment=ft.Alignment.CENTER,
                                    width=64,
                                    height=64,
                                ),
                            ],
                            width=64,
                            height=64,
                        ),
                        ft.Column(
                            [name_text, status_chip], spacing=6, expand=True
                        ),
                        cancel_btn,
                    ],
                    spacing=14,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                progress_bar,
                ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Icon(
                                    ft.Icons.SD_STORAGE,
                                    size=16,
                                    color=ft.Colors.GREY_500,
                                ),
                                mb_text,
                            ],
                            spacing=4,
                        ),
                        ft.Row(
                            [
                                ft.Icon(
                                    ft.Icons.SPEED,
                                    size=16,
                                    color=ft.Colors.GREY_500,
                                ),
                                speed_text,
                            ],
                            spacing=4,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=12,
        ),
    )

    async def watch_progress():
        while downloading["active"]:
            name_text.value = dl.name or "..."
            mb_text.value = dl.mb or "—"
            speed_text.value = dl.speed or "—"
            percent_text.value = dl.percent or "0%"
            q = dl.quality or ""
            status_chip.content.value = f"{t('downloading')} • {q}" if q and q != "—" else t("downloading")
            status_chip.bgcolor = PRIMARY_LIGHT
            status_chip.content.color = PRIMARY
            try:
                frac = float((dl.percent or "0%").strip("%")) / 100
                progress_ring.value = frac
                progress_bar.value = frac
            except ValueError:
                pass
            page.update()
            await asyncio.sleep(0.2)

    def on_done():
        percent_text.value = "100%"
        progress_ring.value = 1
        progress_bar.value = 1
        status_chip.content.value = t("completed")
        status_chip.bgcolor = ft.Colors.GREEN_100
        status_chip.content.color = ft.Colors.GREEN_800
        download_btn.disabled = False
        url_field.value = ""
        refresh_library()
        page.update()

    def classify_error(raw: str) -> str:
        low = (raw or "").lower()
        if "cancelled by user" in low:
            return t("cancelled")
        if "unsupported url" in low or "not a valid url" in low or "invalid url" in low:
            return t("err_invalid_url")
        if "private video" in low or "unavailable" in low or "removed" in low or "not available" in low:
            return t("err_unavailable")
        if "sign in" in low or "not a bot" in low or "cookies" in low:
            return t("err_unavailable")
        if "no space left" in low or "disk quota" in low:
            return t("err_storage")
        if "urlopen" in low or "timed out" in low or "connection" in low or "network" in low:
            return t("err_network")
        return t("err_generic")

    def on_error(err):
        friendly = classify_error(err)
        if "cancelled" in friendly.lower():
            status_chip.content.value = t("cancelled")
            status_chip.bgcolor = ft.Colors.ORANGE_100
            status_chip.content.color = ft.Colors.ORANGE_800
        else:
            status_chip.content.value = t("error")
            status_chip.bgcolor = ft.Colors.RED_100
            status_chip.content.color = ft.Colors.RED_800
            show_error(friendly)
            
        speed_text.value = friendly
        download_btn.disabled = False
        url_field.value = ""
        page.update()

    def run_download(url, quality):
        try:
            final_filename, actual_quality = dl.download(url, quality)
            if final_filename and not dl.is_cancelled:
                settings.set_quality(final_filename, actual_quality)
            downloading["active"] = False
            if not dl.is_cancelled:
                on_done()
        except Exception as e:
            downloading["active"] = False
            traceback.print_exc()
            on_error(str(e))

    def begin_download(url: str, quality: str):
        progress_card.visible = True
        progress_ring.value = 0
        progress_bar.value = 0
        percent_text.value = "0%"
        name_text.value = t("starting")
        mb_text.value = "—"
        speed_text.value = "—"
        status_chip.bgcolor = ft.Colors.GREY_200
        status_chip.content.color = ft.Colors.GREY_700
        status_chip.content.value = t("starting")
        page.update()

        downloading["active"] = True
        page.run_thread(run_download, url, quality)
        page.run_task(watch_progress)

    def show_quality_dialog(url: str, heights: list):
        if heights:
            opts = [("best", "Auto (Ən yüksək)")] + [(str(h), f"{h}p") for h in heights]
        else:
            opts = QUALITY_OPTIONS

        def pick(quality_key):
            def handler(ev):
                quality_dialog.open = False
                page.update()
                begin_download(url, quality_key)
            return handler

        option_buttons = [
            ft.OutlinedButton(
                content=ft.Text(label),
                on_click=pick(key),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            )
            for key, label in opts
        ]

        quality_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(t("quality")),
            content=ft.Column(option_buttons, tight=True, spacing=8, scroll=ft.ScrollMode.AUTO),
        )
        page.show_dialog(quality_dialog)

    def check_and_prompt(url: str):
        loading_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(t("quality")),
            content=ft.Row(
                [ft.ProgressRing(width=20, height=20, stroke_width=3), ft.Text("...")],
                spacing=10,
            ),
        )
        page.show_dialog(loading_dialog)

        heights = dl.probe_qualities(url)

        loading_dialog.open = False
        page.update()

        download_btn.disabled = False
        page.update()
        show_quality_dialog(url, heights)

    def start_download(e):
        if not url_field.value or not url_field.value.strip():
            url_field.value = ""
            show_error(t("err_empty_url"))
            page.update()
            return

        url = url_field.value.strip()
        download_btn.disabled = True
        page.update()
        page.run_thread(check_and_prompt, url)

    download_btn.on_click = start_download

    download_view = ft.Column(
        [
            ft.Row([url_field, download_btn]),
            progress_card,
        ],
        spacing=16,
    )

    logo_badge = ft.Container(
        content=ft.Icon(
            ft.Icons.PLAY_ARROW_ROUNDED, color=ft.Colors.WHITE, size=20
        ),
        width=32,
        height=32,
        bgcolor=PRIMARY,
        border_radius=8,
        alignment=ft.Alignment.CENTER,
    )
    app_title_text = ft.Text(
        t("app_title"), size=20, weight=ft.FontWeight.W_800
    )

    lang_menu_items = []

    def make_lang_click(code):
        def click(e):
            state["lang"] = code
            settings.lang = code
            page.rtl = code == "ar"
            apply_language()
            page.update()

        return click

    for code, label in LANGUAGES:
        lang_menu_items.append(
            ft.PopupMenuItem(content=label, on_click=make_lang_click(code))
        )

    lang_button = ft.PopupMenuButton(
        icon=ft.Icons.LANGUAGE, items=lang_menu_items, tooltip="Language"
    )

    theme_btn = ft.IconButton(
        icon=ft.Icons.LIGHT_MODE
        if state["theme"] == "dark"
        else ft.Icons.DARK_MODE,
        tooltip="Rejim",
    )

    def toggle_theme(e):
        state["theme"] = "light" if state["theme"] == "dark" else "dark"
        settings.theme = state["theme"]
        theme_btn.icon = (
            ft.Icons.LIGHT_MODE
            if state["theme"] == "dark"
            else ft.Icons.DARK_MODE
        )
        apply_theme()
        refresh_library()

    theme_btn.on_click = toggle_theme

    url_launcher = ft.UrlLauncher()

    async def open_github(e):
        url = "https://github.com/testere-development"
        try:
            await url_launcher.launch_url(url)
        except Exception:
            traceback.print_exc()

    github_button = ft.Container(
        content=ft.Image(
            src="https://cdn-icons-png.flaticon.com/512/25/25231.png",
            width=22,
            height=22,
            fit=ft.BoxFit.CONTAIN,
            error_content=ft.Icon(ft.Icons.HUB, size=22),
        ),
        tooltip="GitHub",
        on_click=lambda e: page.run_task(open_github, e),
        padding=8,
        border_radius=8,
        ink=True,
    )

    top_bar_container = ft.Container(
        padding=ft.Padding.symmetric(horizontal=14, vertical=8),
        shadow=ft.BoxShadow(blur_radius=6, color=ft.Colors.BLACK_12),
    )

    top_bar = ft.Row(
        [
            ft.Row([logo_badge, app_title_text], spacing=8),
            ft.Row([github_button, theme_btn, lang_button], spacing=4),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    top_bar_container.content = top_bar

    nav_bar = ft.NavigationBar(
        selected_index=0,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.VIDEO_LIBRARY_OUTLINED,
                selected_icon=ft.Icons.VIDEO_LIBRARY,
                label=t("library"),
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.DOWNLOAD_OUTLINED,
                selected_icon=ft.Icons.DOWNLOAD,
                label=t("download"),
            ),
        ],
    )

    def on_nav_change(e):
        body.content = (
            home_view if e.control.selected_index == 0 else download_view
        )
        page.update()

    nav_bar.on_change = on_nav_change
    page.navigation_bar = nav_bar

    body = ft.Container(content=home_view, expand=True, padding=14)

    root_layout = ft.SafeArea(
        content=ft.Column([top_bar_container, body], expand=True, spacing=0),
        expand=True,
    )

    def apply_theme():
        colors = get_colors()
        page.bgcolor = colors["bg"]
        page.theme_mode = (
            ft.ThemeMode.DARK if state["theme"] == "dark" else ft.ThemeMode.LIGHT
        )

        top_bar_container.bgcolor = colors["card_bg"]
        app_title_text.color = colors["text_main"]
        lang_button.icon_color = colors["text_main"]
        theme_btn.icon_color = colors["text_main"]

        progress_card.bgcolor = colors["card_bg"]
        name_text.color = colors["text_main"]
        mb_text.color = colors["text_sub"]
        speed_text.color = colors["text_sub"]

        nav_bar.bgcolor = colors["card_bg"]

        page.update()

    def apply_language():
        app_title_text.value = t("app_title")
        url_field.label = t("url_label")
        download_btn.content = t("download")
        no_videos_placeholder.content.controls[1].value = t("no_videos")
        nav_bar.destinations[0].label = t("library")
        nav_bar.destinations[1].label = t("download")
        if not downloading["active"]:
            status_chip.content.value = t("waiting")

    page.add(root_layout)
    apply_theme()
    refresh_library()


ft.run(main)
