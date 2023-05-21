import "./App.css";
import { useEffect, useState } from "react";
import Card from "./components/Card";

async function get_prediction(country) {
  country = country.toLowerCase();
  // accepts only 3 letter country code, e.g. isl or usa
  const response = await fetch(`http://localhost:8000/prediction/${country}`);
  const data = await response.json();
  data.location = country.toUpperCase();
  return data;
}

function App() {
  const [data, setData] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      let _data = await get_prediction("isl");
      setData(_data);
    };

    fetchData();
  }, []);

  // runs every 15 minutes
  useEffect(() => {
    const interval = setInterval(async () => {
      let _data = await get_prediction("isl");
      setData(_data);
    }, 1000 * 60 * 15);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <main>
        <h1>
          Slysamat með gervigreind, miðað við rauntíma veður(hitastig og
          vindhraða)
        </h1>
        {data && (
          <Card
            location={data.location}
            prediction={data.prediction}
            percentage_deviation={data.percentage_deviation}
            temperature={data.temp}
            windSpeed={data.wind}
          />
        )}
      </main>
    </div>
  );
}

export default App;
