document.addEventListener('DOMContentLoaded', () => {
  const hamBurger = document.querySelector(".toggle-btn");
  const sidebar = document.querySelector("#sidebar");

  hamBurger.addEventListener("click", function () {
      sidebar.classList.toggle("expand");
  });
});


function updateDateTime() {
  var now = new Date();
  var day = String(now.getDate()).padStart(2, '0');
  var month = String(now.getMonth() + 1).padStart(2, '0'); // Janeiro é 0!
  var year = now.getFullYear();
  var hours = String(now.getHours()).padStart(2, '0');
  var minutes = String(now.getMinutes()).padStart(2, '0');
  var seconds = String(now.getSeconds()).padStart(2, '0');
  
  var datetimeString = `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
  
  document.getElementById("datetime").innerText = datetimeString;
}

setInterval(updateDateTime, 1000); // Atualiza a cada segundo



