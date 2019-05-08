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
  console.log(date_aller);
  if(Date.parse(date_aller)) {
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


var barreDeRecherche = document.getElementById('barreDeRecherche');
barreDeRecherche.addEventListener('submit', function(e){
  resultDA = check['date_aller']();
  resultB = check['budget']();
  resultDR = check['date_retour']();
  if(resultB && resultDA && resultDR){
    console.log('ok ')
  }
  else {
    console.log('not ok');
  }
  //alert('yo');
  e.preventDefault();
});
