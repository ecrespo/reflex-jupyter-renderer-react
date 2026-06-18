import reflex as rx

config = rx.Config(
    app_name="jupyter_renderer_react_demo",
    plugins=[
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.SitemapPlugin(),
        rx.plugins.RadixThemesPlugin(),
    ],
)
