from shapely.geometry import Point

try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
except ImportError:
    Image = TAGS = GPSTAGS = None


def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()


def get_labeled_exif(exif):
    labeled = {}
    for key, val in exif.items():
        labeled[TAGS.get(key)] = val

    return labeled


def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for idx, tag in TAGS.items():
        if tag == "GPSInfo":
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for key, val in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging


def get_decimal_from_dms(dms, ref):
    try:
        degrees = dms[0][0] / dms[0][1]
        minutes = dms[1][0] / dms[1][1] / 60.0
        seconds = dms[2][0] / dms[2][1] / 3600.0
    except TypeError:
        degrees = dms[0]
        minutes = dms[1] / 60.0
        seconds = dms[2] / 3600.0

    if ref in ["S", "W"]:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return degrees + minutes + seconds


def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags["GPSLatitude"], geotags["GPSLatitudeRef"])

    lon = get_decimal_from_dms(geotags["GPSLongitude"], geotags["GPSLongitudeRef"])

    return (lat, lon)


def get_image_geometry(p):
    exif = get_exif(p)
    gps = get_geotagging(exif)
    lat, lon = get_coordinates(gps)

    return Point(lon, lat)
