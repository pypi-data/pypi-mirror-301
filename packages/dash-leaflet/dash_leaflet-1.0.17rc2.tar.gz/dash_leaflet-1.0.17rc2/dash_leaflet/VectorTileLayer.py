# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class VectorTileLayer(Component):
    """A VectorTileLayer component.
Used to load and display vector tile layers on the map. Note that most tile servers require attribution.

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- attribution (string; optional):
    String to be shown in the attribution control, e.g. \"©
    OpenStreetMap contributors\". It describes the layer data and is
    often a legal obligation towards copyright holders and tile
    providers.

- bounds (dict; optional):
    If set, tiles will only be loaded inside the set LatLngBounds.

    `bounds` is a dict with keys:

    - contains (required)

    - equals (required)

    - extend (required)

    - getCenter (required)

    - getEast (required)

    - getNorth (required)

    - getNorthEast (required)

    - getNorthWest (required)

    - getSouth (required)

    - getSouthEast (required)

    - getSouthWest (required)

    - getWest (required)

    - intersects (required)

    - isValid (required)

    - overlaps (required)

    - pad (required)

    - toBBoxString (required)

- className (string; optional):
    A custom class name to assign to the tile layer. Empty by default.

- crossOrigin (boolean | number | string | dict | list; optional):
    Whether the crossOrigin attribute will be added to the tiles. If a
    String is provided, all tiles will have their crossOrigin
    attribute set to the String provided. This is needed if you want
    to access tile pixel data. Refer to CORS Settings for valid String
    values.

- detectRetina (boolean; optional):
    If True and user is on a retina display, it will request four
    tiles of half the specified size and a bigger zoom level in place
    of one to utilize the high resolution.

- disableDefaultEventHandlers (boolean; optional):
    If set to True, default events handlers are not registered.
    [MUTABLE].

- errorTileUrl (string; optional):
    URL to the tile image to show in place of the tile that failed to
    load.

- eventHandlers (dict; optional):
    Object with keys specifying the event type and the value the
    corresponding event handlers. [MUTABLE].

    `eventHandlers` is a dict with keys:

    - add (dict; optional)

        `add` is a dict with keys:


    - autopanstart (dict; optional)

        `autopanstart` is a dict with keys:


    - baselayerchange (dict; optional)

        `baselayerchange` is a dict with keys:


    - click (dict; optional)

        `click` is a dict with keys:


    - contextmenu (dict; optional)

        `contextmenu` is a dict with keys:


    - dblclick (dict; optional)

        `dblclick` is a dict with keys:


    - down (dict; optional)

        `down` is a dict with keys:


    - drag (dict; optional)

        `drag` is a dict with keys:


    - dragend (dict; optional)

        `dragend` is a dict with keys:


    - dragstart (dict; optional)

        `dragstart` is a dict with keys:


    - error (dict; optional)

        `error` is a dict with keys:


    - keydown (dict; optional)

        `keydown` is a dict with keys:


    - keypress (dict; optional)

        `keypress` is a dict with keys:


    - keyup (dict; optional)

        `keyup` is a dict with keys:


    - layeradd (dict; optional)

        `layeradd` is a dict with keys:


    - layerremove (dict; optional)

        `layerremove` is a dict with keys:


    - load (dict; optional)

        `load` is a dict with keys:


    - loading (dict; optional)

        `loading` is a dict with keys:


    - locationerror (dict; optional)

        `locationerror` is a dict with keys:


    - locationfound (dict; optional)

        `locationfound` is a dict with keys:


    - mousedown (dict; optional)

        `mousedown` is a dict with keys:


    - mousemove (dict; optional)

        `mousemove` is a dict with keys:


    - mouseout (dict; optional)

        `mouseout` is a dict with keys:


    - mouseover (dict; optional)

        `mouseover` is a dict with keys:


    - mouseup (dict; optional)

        `mouseup` is a dict with keys:


    - move (dict; optional)

        `move` is a dict with keys:


    - moveend (dict; optional)

        `moveend` is a dict with keys:


    - movestart (dict; optional)

        `movestart` is a dict with keys:


    - overlayadd (dict; optional)

        `overlayadd` is a dict with keys:


    - overlayremove (dict; optional)

        `overlayremove` is a dict with keys:


    - popupclose (dict; optional)

        `popupclose` is a dict with keys:


    - popupopen (dict; optional)

        `popupopen` is a dict with keys:


    - preclick (dict; optional)

        `preclick` is a dict with keys:


    - predrag (dict; optional)

        `predrag` is a dict with keys:


    - remove (dict; optional)

        `remove` is a dict with keys:


    - resize (dict; optional)

        `resize` is a dict with keys:


    - tileabort (dict; optional)

        `tileabort` is a dict with keys:


    - tileerror (dict; optional)

        `tileerror` is a dict with keys:


    - tileload (dict; optional)

        `tileload` is a dict with keys:


    - tileloadstart (dict; optional)

        `tileloadstart` is a dict with keys:


    - tileunload (dict; optional)

        `tileunload` is a dict with keys:


    - tooltipclose (dict; optional)

        `tooltipclose` is a dict with keys:


    - tooltipopen (dict; optional)

        `tooltipopen` is a dict with keys:


    - unload (dict; optional)

        `unload` is a dict with keys:


    - update (dict; optional)

        `update` is a dict with keys:


    - viewreset (dict; optional)

        `viewreset` is a dict with keys:


    - zoom (dict; optional)

        `zoom` is a dict with keys:


    - zoomanim (dict; optional)

        `zoomanim` is a dict with keys:


    - zoomend (dict; optional)

        `zoomend` is a dict with keys:


    - zoomlevelschange (dict; optional)

        `zoomlevelschange` is a dict with keys:


    - zoomstart (dict; optional)

        `zoomstart` is a dict with keys:
 | dict

- featureToLayer (string | dict; optional):
    A function that will be passed a vector-tile feature, the layer
    name, the number of SVG coordinate units per vector-tile unit and
    the feature's style object to create each feature layer.

- fetchOptions (dict; optional):
    Options passed to the `fetch` function when fetching a tile.

- filter (string | dict; optional):
    A function that will be used to decide whether to include a
    feature or not. If specified, it will be passed the vector-tile
    feature, the layer name and the zoom level. The default is to
    include all features.

- keepBuffer (number; optional):
    When panning the map, keep this many rows and columns of tiles
    before unloading them.

- layerOrder (string | dict; optional):
    A function that receives a list of vector-tile layer names and the
    zoom level and returns the names in the order in which they should
    be rendered, from bottom to top. The default is to render all
    layers as they appear in the tile.

- layers (list of strings; optional):
    An array of vector-tile layer names from bottom to top. Layers
    that are missing from this list will not be rendered. The default
    is to render all layers as they appear in the tile.

- loading_state (dict; optional):
    Dash loading state information.

- maxDetailZoom (number; optional):
    Specify zoom range in which tiles are loaded. Tiles will be
    rendered from the same data for Zoom levels outside the range.

- maxNativeZoom (number; optional):
    Maximum zoom number the tile source has available. If it is
    specified, the tiles on all zoom levels higher than maxNativeZoom
    will be loaded from maxNativeZoom level and auto-scaled.

- maxZoom (number; optional):
    The maximum zoom level up to which this layer will be displayed
    (inclusive).

- minDetailZoom (number; optional):
    Specify zoom range in which tiles are loaded. Tiles will be
    rendered from the same data for Zoom levels outside the range.

- minNativeZoom (number; optional):
    Minimum zoom number the tile source has available. If it is
    specified, the tiles on all zoom levels lower than minNativeZoom
    will be loaded from minNativeZoom level and auto-scaled.

- minZoom (number; optional):
    The minimum zoom level down to which this layer will be displayed
    (inclusive).

- n_loads (number; optional):
    An integer that represents the number of times that the load event
    has fired.

- noWrap (boolean; optional):
    Whether the layer is wrapped around the antimeridian. If True, the
    GridLayer will only be displayed once at low zoom levels. Has no
    effect when the map CRS doesn't wrap around. Can be used in
    combination with bounds to prevent requesting tiles outside the
    CRS limits.

- opacity (number; optional):
    The layer opacity. [MUTABLE].

- pane (string; optional):
    Map pane where the layer will be added.

- referrerPolicy (boolean | number | string | dict | list; optional):
    Whether the referrerPolicy attribute will be added to the tiles.
    If a String is provided, all tiles will have their referrerPolicy
    attribute set to the String provided. This may be needed if your
    map's rendering context has a strict default but your tile
    provider expects a valid referrer (e.g. to validate an API token).
    Refer to HTMLImageElement.referrerPolicy for valid String values.

- style (string | dict; optional):
    Either a single style object for all features on all layers or a
    function that receives the vector-tile feature, the layer name and
    the zoom level and returns the appropriate style options.

- subdomains (string | list of strings; optional):
    Subdomains of the tile service. Can be passed in the form of one
    string (where each letter is a subdomain name) or an array of
    strings.

- tileSize (number; optional):
    Width and height of tiles in the grid. Use a number if width and
    height are equal, or L.point(width, height) otherwise.

- tms (boolean; optional):
    If True, inverses Y axis numbering for tiles (turn this on for TMS
    services).

- updateInterval (number; optional):
    Tiles will not update more than once every updateInterval
    milliseconds when panning.

- updateWhenIdle (boolean; optional):
    Load new tiles only when panning ends. True by default on mobile
    browsers, in order to avoid too many requests and keep smooth
    navigation. False otherwise in order to display new tiles during
    panning, since it is easy to pan outside the keepBuffer option in
    desktop browsers.

- updateWhenZooming (boolean; optional):
    By default, a smooth zoom animation (during a touch zoom or a
    flyTo()) will update grid layers every integer zoom level. Setting
    this option to False will update the grid layer only when the
    smooth animation ends.

- url (string; optional):
    The URL template in the form
    'https://{s}.example.com/tiles/{z}/{x}/{y}.pbf'.

- vectorTileLayerStyles (dict; optional):
    This works like the same option for `Leaflet.VectorGrid`. Ignored
    if style is specified.

- zIndex (number; optional):
    The layer zIndex. [MUTABLE].

- zoomOffset (number; optional):
    The zoom number used in tile URLs will be offset with this value.

- zoomReverse (boolean; optional):
    If set to True, the zoom number used in tile URLs will be reversed
    (maxZoom - zoom instead of zoom)."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_leaflet'
    _type = 'VectorTileLayer'
    @_explicitize_args
    def __init__(self, opacity=Component.UNDEFINED, className=Component.UNDEFINED, attribution=Component.UNDEFINED, pane=Component.UNDEFINED, eventHandlers=Component.UNDEFINED, crossOrigin=Component.UNDEFINED, zIndex=Component.UNDEFINED, bounds=Component.UNDEFINED, minZoom=Component.UNDEFINED, maxZoom=Component.UNDEFINED, updateWhenIdle=Component.UNDEFINED, subdomains=Component.UNDEFINED, errorTileUrl=Component.UNDEFINED, zoomOffset=Component.UNDEFINED, tms=Component.UNDEFINED, zoomReverse=Component.UNDEFINED, detectRetina=Component.UNDEFINED, referrerPolicy=Component.UNDEFINED, tileSize=Component.UNDEFINED, updateWhenZooming=Component.UNDEFINED, updateInterval=Component.UNDEFINED, maxNativeZoom=Component.UNDEFINED, minNativeZoom=Component.UNDEFINED, noWrap=Component.UNDEFINED, keepBuffer=Component.UNDEFINED, url=Component.UNDEFINED, featureToLayer=Component.UNDEFINED, fetchOptions=Component.UNDEFINED, filter=Component.UNDEFINED, layerOrder=Component.UNDEFINED, layers=Component.UNDEFINED, minDetailZoom=Component.UNDEFINED, maxDetailZoom=Component.UNDEFINED, style=Component.UNDEFINED, vectorTileLayerStyles=Component.UNDEFINED, id=Component.UNDEFINED, loading_state=Component.UNDEFINED, disableDefaultEventHandlers=Component.UNDEFINED, n_loads=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'attribution', 'bounds', 'className', 'crossOrigin', 'detectRetina', 'disableDefaultEventHandlers', 'errorTileUrl', 'eventHandlers', 'featureToLayer', 'fetchOptions', 'filter', 'keepBuffer', 'layerOrder', 'layers', 'loading_state', 'maxDetailZoom', 'maxNativeZoom', 'maxZoom', 'minDetailZoom', 'minNativeZoom', 'minZoom', 'n_loads', 'noWrap', 'opacity', 'pane', 'referrerPolicy', 'style', 'subdomains', 'tileSize', 'tms', 'updateInterval', 'updateWhenIdle', 'updateWhenZooming', 'url', 'vectorTileLayerStyles', 'zIndex', 'zoomOffset', 'zoomReverse']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'attribution', 'bounds', 'className', 'crossOrigin', 'detectRetina', 'disableDefaultEventHandlers', 'errorTileUrl', 'eventHandlers', 'featureToLayer', 'fetchOptions', 'filter', 'keepBuffer', 'layerOrder', 'layers', 'loading_state', 'maxDetailZoom', 'maxNativeZoom', 'maxZoom', 'minDetailZoom', 'minNativeZoom', 'minZoom', 'n_loads', 'noWrap', 'opacity', 'pane', 'referrerPolicy', 'style', 'subdomains', 'tileSize', 'tms', 'updateInterval', 'updateWhenIdle', 'updateWhenZooming', 'url', 'vectorTileLayerStyles', 'zIndex', 'zoomOffset', 'zoomReverse']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(VectorTileLayer, self).__init__(**args)
