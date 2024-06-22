import flask, numpy, requests, os
from dotenv import load_dotenv

load_dotenv()

MUNICIPALITIES_BASE_URL = "https://opendata.resas-portal.go.jp/api/v1/cities"
COORDINATE_BASE_URL = "https://msearch.gsi.go.jp/address-search/AddressSearch"
ELEVATION_BASE_URL = "http://cyberjapandata2.gsi.go.jp/general/dem/scripts/getelevation.php"

COORDINATE_LIST = [
    {"lat":44.0,"lon":142.0+15/60},
    {"lat":40.0,"lon":140.0+50/60},
    {"lat":40.0,"lon":140.0+50/60},
    {"lat":40.0,"lon":140.0+50/60},
    {"lat":40.0,"lon":140.0+50/60},
    {"lat":40.0,"lon":140.0+50/60},
    {"lat":36.0,"lon":139.0+50/60},
    {"lat":36.0,"lon":139.0+50/60},
    {"lat":36.0,"lon":139.0+50/60},
    {"lat":36.0,"lon":139.0+50/60},
    {"lat":36.0,"lon":139.0+50/60},
    {"lat":36.0,"lon":139.0+50/60},
    {"lat":36.0,"lon":139.0+50/60},
    {"lat":36.0,"lon":139.0+50/60},
    {"lat":36.0,"lon":138.0+30/60},
    {"lat":36.0,"lon":137.0+10/60},
    {"lat":36.0,"lon":137.0+10/60},
    {"lat":36.0,"lon":136.0},
    {"lat":36.0,"lon":138.0+30/60},
    {"lat":36.0,"lon":138.0+30/60},
    {"lat":36.0,"lon":137.0+10/60},
    {"lat":36.0,"lon":138.0+30/60},
    {"lat":36.0,"lon":137.0+10/60},
    {"lat":36.0,"lon":136.0},
    {"lat":36.0,"lon":136.0},
    {"lat":36.0,"lon":136.0},
    {"lat":36.0,"lon":136.0},
    {"lat":36.0,"lon":134.0+20/60},
    {"lat":36.0,"lon":136.0},
    {"lat":36.0,"lon":136.0},
    {"lat":36.0,"lon":134.0+20/60},
    {"lat":36.0,"lon":132.0+10/60},
    {"lat":36.0,"lon":134.0+20/60},
    {"lat":36.0,"lon":132.0+10/60},
    {"lat":36.0,"lon":132.0+10/60},
    {"lat":36.0,"lon":133.0+30/60},
    {"lat":36.0,"lon":133.0+30/60},
    {"lat":36.0,"lon":133.0+30/60},
    {"lat":36.0,"lon":133.0+30/60},
    {"lat":33.0,"lon":131.0},
    {"lat":33.0,"lon":131.0},
    {"lat":33.0,"lon":129.0+30/60},
    {"lat":33.0,"lon":131.0},
    {"lat":33.0,"lon":131.0},
    {"lat":33.0,"lon":131.0},
    {"lat":33.0,"lon":131.0},
    {"lat":26.0,"lon":127.0+30/60}
]

MUNICIPALITIES_POPULATION = requests.get("http://api.e-stat.go.jp/rest/3.0/app/json/getStatsData", params={
    "appId": os.environ.get("APP_ID").encode("utf-8"),
    "lang": "J",
    "statsDataId": "0003445078",
    "metaGetFlg": "Y",
    "cntGetFlg": "N",
    "explanationGetFlg": "Y",
    "annotationGetFlg": "Y",
    "sectionHeaderFlg": "1",
    "replaceSpChars": "0"
}).json()

MUNICIPALITIES_POPULATION_DATA = {}
for i in MUNICIPALITIES_POPULATION["GET_STATS_DATA"]["STATISTICAL_DATA"]["DATA_INF"]["VALUE"]:
    if i["@cat01"] == "0":
        MUNICIPALITIES_POPULATION_DATA[i["@area"]] = i["$"]

def make_A_array(n):
    A0 = 1 + (n**2)/4. + (n**4)/64.
    A1 = -(3./2)*(n - (n**3)/8. - (n**5)/64.)
    A2 = (15./16)*(n**2 - (n**4)/4.)
    A3 = -(35./48)*(n**3 - (5./16)*(n**5))
    A4 = (315./512)*(n**4)
    A5 = -(693./1280)*(n**5)
    return numpy.array([A0, A1, A2, A3, A4, A5])

def make_alpha_array(n):
    a0 = numpy.nan
    a1 = (1./2)*n - (2./3)*(n**2) + (5./16)*(n**3) + (41./180)*(n**4) - (127./288)*(n**5)
    a2 = (13./48)*(n**2) - (3./5)*(n**3) + (557./1440)*(n**4) + (281./630)*(n**5)
    a3 = (61./240)*(n**3) - (103./140)*(n**4) + (15061./26880)*(n**5)
    a4 = (49561./161280)*(n**4) - (179./168)*(n**5)
    a5 = (34729./80640)*(n**5)
    return numpy.array([a0, a1, a2, a3, a4, a5])

def calc_xy(phi_deg, lambda_deg, pre_code):
    """ Convert latitude and longitude to plane rectangular coordinates
    (phi_deg, lambda_deg): Latitude and longitude to be converted [degrees] (not minutes and seconds, but decimal)
    x, y: Converted plane rectangular coordinates [m]
    """
    phi0_deg, lambda0_deg = COORDINATE_LIST[pre_code]["lat"], COORDINATE_LIST[pre_code]["lon"]
    phi_rad, lambda_rad, phi0_rad, lambda0_rad = numpy.deg2rad(phi_deg), numpy.deg2rad(lambda_deg), numpy.deg2rad(phi0_deg), numpy.deg2rad(lambda0_deg)

    m0, a = 0.9999, 6378137.
    F = 298.257222101

    n = 1./(2*F - 1)
    A_array, alpha_array = make_A_array(n), make_alpha_array(n)

    A_ = ((m0*a)/(1.+n))*A_array[0]
    S_ = ((m0*a)/(1.+n))*(A_array[0]*phi0_rad + numpy.dot(A_array[1:], numpy.sin(2*phi0_rad*numpy.arange(1, 6))))

    lambda_c, lambda_s = numpy.cos(lambda_rad - lambda0_rad), numpy.sin(lambda_rad - lambda0_rad)

    t = numpy.sinh(numpy.arctanh(numpy.sin(phi_rad)) - ((2*numpy.sqrt(n))/(1+n))*numpy.arctanh(((2*numpy.sqrt(n))/(1+n))*numpy.sin(phi_rad)))
    t_ = numpy.sqrt(1 + t**2)

    xi2, eta2 = numpy.arctan(t/lambda_c), numpy.arctanh(lambda_s/t_)

    x = A_*(xi2 + numpy.sum(numpy.multiply(alpha_array[1:], numpy.multiply(numpy.sin(2*xi2*numpy.arange(1, 6)), numpy.cosh(2*eta2*numpy.arange(1, 6)))))) - S_
    y = A_*(eta2 + numpy.sum(numpy.multiply(alpha_array[1:], numpy.multiply(numpy.cos(2*xi2*numpy.arange(1, 6)), numpy.sinh(2*eta2*numpy.arange(1, 6))))))

    return x, y

app = flask.Flask(__name__, static_folder=".", static_url_path="")

@app.route("/")
def index():
    """Return hello world"""
    return "hello world"

@app.route("/api/<int:pref_code>")
def api(pref_code):
    """Return city data for given prefecture code"""
    status = "ERROR"
    result = []

    if not 1 <= pref_code <= len(COORDINATE_LIST):
        return flask.jsonify(status=status, result=["pref_code does not exist"])

    # Fetch municipalities data
    try:
        municipalities_res = requests.get(MUNICIPALITIES_BASE_URL, headers={"X-API-KEY":os.environ.get("API_KEY")}, params={"prefCode": pref_code})
    except requests.RequestException as e:
        return flask.jsonify(status=status, result=[f"response's status from {MUNICIPALITIES_BASE_URL} is not success: {str(e)}"])

    municipalities_res = municipalities_res.json()

    if "statusCode" in municipalities_res:
        return flask.jsonify(status=status, result=[f"response's status code from {MUNICIPALITIES_BASE_URL} is {municipalities_res['statusCode']}"])

    # Process each city in the response
    for city in municipalities_res["result"]:
        if city["bigCityFlag"] == "2":
            continue

        try:
            coordinate_res = requests.get(COORDINATE_BASE_URL, params={"q": city["cityName"]}).json()
        except requests.RequestException as e:
            return flask.jsonify(status=status, result=[f"response's status from {COORDINATE_BASE_URL} is not success: {str(e)}"])

        check_id = str(city["cityCode"]) if str(city["cityCode"])[0] != "0" else str(city["cityCode"])[1:]
        data = [i for i in coordinate_res if i["properties"]["addressCode"] == check_id]

        lon, lat, x, y = None, None, 0, 0
        if len(data) > 1:
            for j in data:
                if "役所" in j["properties"]["title"] or "役場" in j["properties"]["title"]:
                    lon, lat = j["geometry"]["coordinates"][0], j["geometry"]["coordinates"][1]
                    x, y = calc_xy(lat, lon, pref_code-1)
                    break
        elif len(data) == 1:
            lon, lat = data[0]["geometry"]["coordinates"][0], data[0]["geometry"]["coordinates"][1]
            x, y = calc_xy(lat, lon, pref_code-1)
        else:
            continue

        # Fetch elevation data
        try:
            elevation_res = requests.get(ELEVATION_BASE_URL, params={"lon": lon, "lat": lat, "outtype": "JSON"}).json()
        except requests.RequestException as e:
            return flask.jsonify(status=status, result=[f"response's status from {ELEVATION_BASE_URL} is not success: {str(e)}"])

        result.append(
            {
                "id": city["cityCode"],
                "name": city["cityName"],
                "coordinates": {"x": x, "y": y, "elevation": elevation_res["elevation"]},
                "population": int(MUNICIPALITIES_POPULATION_DATA.get(city["cityCode"], 0)),
            }
        )

    status = "SUCCESS"
    return flask.jsonify(status=status, result=result)

if __name__ == "__main__":
    app.run()
