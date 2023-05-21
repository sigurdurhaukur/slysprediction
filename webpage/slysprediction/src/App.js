import "./App.css";
import { useEffect, useState } from "react";
import Card from "./components/Card";

async function get_prediction(country) {
  country = country.toLowerCase();
  // accepts only 3 letter country code, e.g. isl or usa
  const response = await fetch(
    `http://localhost:8000/prediction/${country}/live`
  );
  const data = await response.json();
  data.location = country.toUpperCase();
  return data;
}

function App() {
  const [islData, setIslData] = useState({});
  const [usaData, setUsaData] = useState({});

  const fetchData = async (country) => {
    let _data = await get_prediction(country);

    if (country === "isl") {
      setIslData(_data);
      return;
    } else if (country === "usa") {
      setUsaData(_data);
      return;
    }
  };

  useEffect(() => {
    fetchData("isl");
    fetchData("usa");

    console.log(islData, usaData);
  }, []);

  // runs every 15 minutes
  useEffect(() => {
    const interval = setInterval(async () => {
      fetchData("isl");
      fetchData("usa");
    }, 1000 * 2);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <main>
        <h1>
          Slysamat með gervigreind, útfrá rauntíma veðri (hitastigi og
          vindhraða)
        </h1>
        {islData && (
          <Card
            location={islData.location}
            prediction={islData.prediction}
            percentage_deviation={islData.percentage_deviation}
            temperature={islData.temp}
            windSpeed={islData.wind}
          />
        )}
        {usaData && (
          <Card
            location={usaData.location}
            prediction={usaData.prediction}
            percentage_deviation={usaData.percentage_deviation}
            temperature={usaData.temp}
            windSpeed={usaData.wind}
          />
        )}
      </main>
    </div>
  );
}

export default App;
