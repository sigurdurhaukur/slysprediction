to run the server

```bash
uvicorn main:app --reload
```

and then go to http://localhost:8000

routes:

- /prediction/isl (get)
- /prediction/us (get)

`/prediction/isl` returns a json object with the prediction of amount of accidents for this month based on the average temperature along with the current temperature and wind-speed, and the average amount of accidents per month in Iceland.

`/prediction/usa` returns a json object with the prediction of amount of accidents for this month based on the average temperature and wind speed along with the current temperature and wind-speed, and the average amount of accidents per month in USA.

Example response from `/prediction/isl`:

```json
{
  "temp": 6.89622641509434,
  "wind": 8.415094339622641,
  "prediction": 272.2669871939281,
  "percentage_deviation": 10.677637070702486,
  "average_accidents_per_month": 246
}
```

Example response from `/prediction/usa`:

```json
{
  "temp": 6.89622641509434,
  "wind": 8.415094339622641,
  "prediction": 27546.254049224797,
  "percent_deviation": -86.3904596503899,
  "average_accidents_per_month": 4216.75
}
```
