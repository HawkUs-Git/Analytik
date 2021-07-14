data = {}

function doesContain(a, obj){
  e = false;
  a.forEach(function(i){
    if (i.private_key == obj.private_key){
      e = true;
    }
  })
  return e
}

var saves;

if (localStorage.getItem('e') == null){
  localStorage.setItem('e', '[]')
}

JSON.parse(localStorage.getItem('e')).forEach(function(i){
  document.querySelector('.recents').innerHTML += `<div class="recent" onClick='login_with_key("`+i.id+`")'>
    `+i.name+` <span class="recent-key">`+i.id+`</span>
  </div>  `
})


function doTheThing(res){
      document.querySelector('.browser-hit-count.chrome').innerHTML = res.load.app_hits.Chrome
      document.querySelector('.browser-hit-count.edge').innerHTML = res.load.app_hits.Edge
      document.querySelector('.browser-hit-count.safari').innerHTML = res.load.app_hits.Safari
      document.querySelector('.browser-hit-count.firefox').innerHTML = res.load.app_hits.Firefox

      document.querySelector('#total-views').innerHTML = res.load.app_hits.Firefox + res.load.app_hits.Safari + res.load.app_hits.Edge + res.load.app_hits.Chrome

      document.querySelector('#unique-views').innerHTML = res.load.app_user_hits.length

      document.querySelector('.app_title').innerHTML = res.load.app_name

      res.load.app_user_hits.forEach(function(item){
        document.querySelector('.users-dhdp').innerHTML += "<li>" + item + "</li>"
      })
}

function login_with_key(key){
  fetch('../loginkey', {
    'method': "POST",
    'body': `{"key": "`+key+`"}`
  })
  .then(response => response.json())
  .then(res => {
    document.querySelector('.login').style.display = "none"
    document.querySelector('.dashboard').style.display = "block"

    document.querySelector('.container').className = "dash-container"

    doTheThing(res)
  })
}

function login(){
  fetch('../loginapi', {
    "method": "POST",
    'body': JSON.stringify({
      'password': document.querySelector('#password').value,
      'key': document.querySelector('#apikey').value
    })
  })
  .then(response => response.json())
  .then(res => {
    console.log(res.status)
    if (res.status == true){

      saves = JSON.parse(localStorage.getItem('e'))
      
      if (doesContain(saves, {'id': res.load.private_key, 'name': res.load.app_name}) == false){
        saves.push({'id': res.load.private_key, 'name': res.load.app_name})
      }

      localStorage.setItem('e', JSON.stringify(saves))

      document.querySelector('.login').style.display = "none"
      document.querySelector('.dashboard').style.display = "block"

      document.querySelector('.container').className = "dash-container"

      data = res

      doTheThing(res)
    }
    else{
      document.querySelector('.landing-button-poggers').innerHTML = "login"
      alert('Something went wrong. Perhaps wrong password or api key?')
    }
  })
}