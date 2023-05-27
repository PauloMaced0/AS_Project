const districtsOfPortugal = [
  "Aveiro",
  "Beja",
  "Braga",
  "Bragança",
  "Castelo Branco",
  "Coimbra",
  "Évora",
  "Faro",
  "Guarda",
  "Leiria",
  "Lisboa",
  "Portalegre",
  "Porto",
  "Santarém",
  "Setúbal",
  "Viana do Castelo",
  "Vila Real",
  "Viseu",
  "Açores",
  "Madeira"
];

const inputDistrict = document.getElementById('inputdistrict');

districtsOfPortugal.forEach(district => {
  const option = document.createElement("option");
  option.text = district;
  inputDistrict.add(option);
});

function setDateInput() {
  const currentDate = new Date();
  const year = currentDate.getFullYear();
  let month = (currentDate.getMonth() + 1).toString().padStart(2, '0');
  let day = currentDate.getDate().toString().padStart(2, '0');

  const formattedDate = `${year}-${month}-${day}`;
  document.getElementById("inputDate").value = formattedDate;
}

function setTimeinput() {
  const currentDate = new Date();
  let hours = currentDate.getHours().toString().padStart(2, '0');
  let minutes = currentDate.getMinutes().toString().padStart(2, '0');

  const formattedTime = `${hours}:${minutes}`;
  document.getElementById("inputTime").value = formattedTime;
}

setDateInput();
setTimeinput();


