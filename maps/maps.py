import os
from flask import Flask, render_template, request, jsonify
from google.cloud import aiplatform
from googlemaps import Client

app = Flask(__name__)

# 環境変数から設定を読み込む
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
PROJECT_ID = os.environ.get("PROJECT_ID")
# Geminiモデル名。必要に応じて変更してください
GEMINI_MODEL_NAME = "models/gemini-1.5-flash-002"

# Google Maps Clientのインスタンス化
gmaps = Client(key=GOOGLE_MAPS_API_KEY)

# Vertex AIのクライアントインスタンス化
aiplatform.init(project=PROJECT_ID)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        search_query = request.form["search"]

        # Geminiを使用して検索クエリを処理する
        response = aiplatform.predict(
            endpoint="projects/" + PROJECT_ID + "/locations/us-central1/endpoints/" + GEMINI_MODEL_NAME, # 適切なエンドポイント名を設定してください。
            instances=[{"content": search_query, "parameters": {"temperature": 0.2}}],  # temperatureは調整してください
        )
        places_api_query = response.predictions[0]["text"] # 予想されるPlaces APIのクエリを抽出。モデルの出力に合わせて変更してください


        try:
            places_result = gmaps.places(query=places_api_query, location="current") # current locationはユーザーの現在地を取得する必要があります。IPアドレスから取得するなどの方法が必要
            # 地図の更新に必要な情報をplaces_resultから抽出します。例：
            map_center = places_result['results'][0]['geometry']['location']
            # ... 他の必要な情報も抽出 ...
            return jsonify({"success": True, "map_center": map_center, "places_result": places_result}) # フロントエンドにJSONで情報を返す
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})

    # 初期表示時の現在地取得処理。この部分はIPアドレスから取得するなど、適切な実装が必要です
    try:
        current_location = gmaps.geolocate()  # 代替手段が必要
        initial_map_center = current_location['location']
    except Exception as e:
        initial_map_center = {'lat': 35.6895, 'lng': 139.6917} # デフォルト位置(東京)

    return render_template("index.html", initial_map_center=initial_map_center)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))