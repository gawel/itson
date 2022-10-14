import time
import requests
import itson


def report_url(path):
    return 'https://www.surf-report.com/' + path.lstrip('/')


known_spots = {
    "Les Sables d'Olonnes": '/reports/sables-olonne-archives-s1092.html',
    "Bud Bud": "/reports/longeville-mer-archives-s1095.html",
    "La Torche": "/reports/la-torche-archives-s1040.html",
}


def main():
    reports = []
    for spot, path in known_spots.items():
        time.sleep(.3)
        resp = requests.get(report_url(path), verify=False)
        rpath = path.split('-archives-')[0]
        for line in resp.text.split():
            if "href" in line and rpath in line:
                reports.extend([
                    (spot, p, p[len(rpath) + 1:].split('-')[:3])
                    for p in line.split('"')
                    if p.startswith(rpath) and not p.startswith(path)
                ])
    for spot, path, date in reports:
        date = '%s-%s-%s' % tuple(reversed(date))
        itson.db.update(
            dict(report_url=report_url(path)),
            (itson.Session.date == date) & (itson.Session.spot == spot)
        )


if __name__ == '__main__':
    main()
