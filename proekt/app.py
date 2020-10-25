import flask  # сперва подключим модуль
# from flask import Flask
import data

app = flask.Flask(__name__)  # объявим экземпляр фласка


@app.route('/')
def main():
    tours = data.tours
    description = data.description
    subtitle = data.subtitle
    departures = data.departures
    return flask.render_template(
        'index.html',
        tours=tours,
        description=description,
        subtitle=subtitle,
        departures=departures
    )


@app.route('/tours/<int:id>')
def tour_view(id):
    current_tour = data.tours.get(id)
    if current_tour is None:  # проверка страницы
        flask.abort(404)

    departure = data.departures[current_tour['departure']]
    return flask.render_template(
        'tour.html',
        tour=current_tour,
        departure=departure,
        title=data.title,
        departures=data.departures
    )


@app.route('/departures/<departure>')
def departures_view(departure):
    departures = data.departures
    departure_full_name = data.departures.get(departure)
    if departure_full_name is None:
        flask.abort(404)
    filtered_tours = {}
    min_price = float('inf')
    max_price = float('-inf')
    min_nights = float('inf')
    max_nights = float('-inf')

    for id, tour in data.tours.items():
        if tour['departure'] != departure:
            continue
        filtered_tours[id] = tour

        if tour['price'] < min_price:
            min_price = tour['price']
        if tour['price'] > max_price:
            max_price = tour['price']
        if tour['nights'] < min_nights:
            min_nights = tour['nights']
        if tour['nights'] > max_nights:
            max_nights = tour['nights']

    return flask.render_template(
        'departure.html',
        departure_full_name=departure_full_name,
        departures=departures,
        tours=filtered_tours,
        min_price=min_price,
        max_price=max_price,
        min_nights=min_nights,
        max_nights=max_nights
    )

# если необходимо будет запусть код в дебаг режиме, то нужно раскоментировать ниже код


if __name__ == '__main__':
    app.run()
