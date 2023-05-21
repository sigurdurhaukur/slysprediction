export default function Card({
  location,
  prediction,
  percentage_deviation,
  temperature,
  windSpeed,
}) {
  return (
    <div className="card">
      <div className="card-body">
        <h5 className="card-title">{location}</h5>
        <p className="card-text">
          Fjöldi slysa í mánuðnum: {prediction} <br />
          Prósentu frávik frá meðaltali: {percentage_deviation}% <br />
          Rauntíma hitastig: {temperature} <br />
          Rauntíma vindhraði: {windSpeed}
        </p>
      </div>
    </div>
  );
}
