affichage_resultats = function(data) {
  document.getElementById('liste_resultats').innerHTML += "<li>data</li><br /><br />";
}

for(var i = 0; i < 8; i++) {
  affichage_resultats("yo");
}
