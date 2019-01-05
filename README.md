# short-linker-django2

Default user/pass: test/test

Little app for short and redirect links (Upwork work)
1. Login page: https://yadi.sk/i/gB1fGAGRIfzACw
2. Register page: https://yadi.sk/i/aqc8oek1Y4g6DQ
3. Index page: https://yadi.sk/i/AY00VAm9jLSgJA
4. Add link: https://yadi.sk/i/InWR5Vcnd7XCNA
5. Settings page: https://yadi.sk/i/7ajuv_O5ZfjIwA


Urls:
1. /linker/login/ - login page
2. /linker/register/ - register page
3. /linker/profile/<profile_username>/ - page, where you can see your links.
4. /linker/profile/add_link/ - page, where you can add some links (login requiered).
5. /linker/profile/delete_link/<profile_username>/<int:id>/ - automated view for deleting links (login requiered).
6. /linker/settings/ - page, where you can update your personal info.
7. /linker/page/<page_id>/ - redirect wrapper.
8. /linker/logout/ - logout page (login required).

generate_redirect.py - simple tool for creating unique url.
