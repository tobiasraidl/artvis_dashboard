import dash_bootstrap_components as dbc
from dash import html, callback
from dash.dependencies import Input, Output

def Navbar():
    navbar = dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand("ArtVis Dashboard", href="#"),

                dbc.Nav(
                    [
                        # Page links
                        dbc.NavItem(dbc.NavLink("Exhibitions", href="/")),
                        dbc.NavItem(dbc.NavLink("Artist Migration", href="/artist-migration")),
                    ],
                    className="ml-auto",  # Aligns the nav items to the right
                    navbar=True,
                ),
            ]
        ),
        color="#121212",
        dark=True,
        className="mb-4"
    )
        
    return navbar