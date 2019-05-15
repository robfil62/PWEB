var check = {};

check['budget'] = function() {
  var budget = document.getElementById('budget');
  budgetValue = parseInt(budget.value);
  if(!isNaN(budgetValue) && budgetValue > 0){
  //  alert(budgetValue);
    return true;
  }
  else {
    //alert(budgetValue);
    return false;
  }
}

check['date_aller'] = function() {
  var date_aller = document.getElementById('date_aller').value;
  var date = new Date();
  console.log('date = ', date);
  console.log(date_aller);
  if(Date.parse(date_aller)&& date_aller < date) {
    console.log('dateOk');
    return true;
  }
  else {
    console.log(('dateNoOk'));
    return false;
  }
}

check['date_retour'] = function() {
  var date_retour = document.getElementById('date_retour').value;
  console.log(date_retour);
  if(Date.parse(date_retour)) {
    console.log('dateOk');
    return true;
  }
  else {
    console.log(('dateNoOk'));
    return false;
  }
}

check['lieu'] = function() {
  var lieu = document.getElementById('lieu').value;
  if(lieu.length > 0) {
    console.log('lieuOk');
    return true;
  }
  else {
    console.log('lieuNotOk');
    return false;
  }
}


var barreDeRecherche = document.getElementById('barreDeRecherche');
barreDeRecherche.addEventListener('submit', function(e){
  resultDA = check['date_aller']();
  resultB = check['budget']();
  resultDR = check['date_retour']();
  resultL = check['lieu']();
  if(resultB && resultDA && resultDR && resultL){
    console.log('ok ')
    //var xhr = new XMLHttpRequest();
    //var budget = encodeURIComponent(document.getElementById('budget').value);
    //var date_aller = encodeURIComponent(document.getElementById('date_aller').value);
    //var date_retour = encodeURIComponent(document.getElementById('date_retour').value);
    //var lieu = encodeURIComponent(document.getElementById('lieu').value);
    //xhr.open('GET', 'http://localhost:5000/Odyssee/search?budget=' + budget + '&date_aller=' + date_aller + '&date_retour=' + date_retour +'&lieu=' + lieu, false);
    //xhr.send(null);
  }
  else {
    console.log('not ok');
  }
  //alert('yo');
  e.preventDefault();
});
