# Django
from django.templatetags.static import static

# Alliance Auth
from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class SlateThemeHook(ThemeHook):
    """
    Bootswatch Slate Theme
    https://bootswatch.com/slate/
    """

    def __init__(self):
        ThemeHook.__init__(
            self,
            "Slate",
            "Shades of gunmetal gray",
            css=[
                {
                    "url": "https://cdnjs.cloudflare.com/ajax/libs/bootswatch/5.3.3/slate/bootstrap.min.css",
                    "integrity": "sha512-3EVe7TjxthzbTGfmRFr7zIvHjDWW7viFDgKOoTJ7S5IIrrKVN5rbPVjj0F7nT6rTyAkURnzwoujxlALvHoO9jw==",
                },
                {"url": static("eunicore/theme/slate/css/tweaks.css")},
            ],
            js=[
                {
                    "url": "https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.11.8/umd/popper.min.js",
                    "integrity": "sha512-TPh2Oxlg1zp+kz3nFA0C5vVC6leG/6mm1z9+mA81MI5eaUVqasPLO8Cuk4gMF4gUfP5etR73rgU/8PNMsSesoQ==",
                },
                {
                    "url": "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.3/js/bootstrap.min.js",
                    "integrity": "sha512-ykZ1QQr0Jy/4ZkvKuqWn4iF3lqPZyij9iRv6sGqLRdTPkY69YX6+7wvVGmsdBbiIfN/8OdsI7HABjvEok6ZopQ==",
                },
            ],
            header_padding="4.5em",
        )


@hooks.register("theme_hook")
def register_slate_hook():
    return SlateThemeHook()
