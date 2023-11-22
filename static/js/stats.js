const userEmail = document.getElementById("userE")
const userScore = document.getElementById("userH")
const userLatest = document.getElementById("userL")
const userAverage = document.getElementById("userA")
const userLowest = document.getElementById("userL2")
const userCreation = document.getElementById("userC")
const userGames = document.getElementById("userG")
const userPosition = document.getElementById("userP")
const refresh = document.getElementById("resetBtn")

document.querySelectorAll(".user-username").forEach((element) => {
  element.addEventListener("click", (event) => {
    const username = event.target.getAttribute("data-username");
    const userId = event.target.getAttribute("data-userid");
    fetch(`/userstats/${userId}/`)
      .then((response) => response.json())
      .then((data) => {
        const creationDate = new Date(data.created_at);
        const options = {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: 'numeric',
            minute: '2-digit',
            hour12: true,
            timeZoneName: 'short',
            hourCycle: 'h12', // use "h12" instead of "h23" to display hours in 1-12 format
          };          
        const formattedCreationDate = creationDate.toLocaleString('en-US', options)
          .replace(' at ', ', ') // replace " at " with a comma and a space
          .replace('PM', 'p.m.')
          .replace('PDT', '') // replace "PM" with "p.m."
        formattedCreationDate
        userEmail.innerText = `// here are ${username}'s statistics:`
        userScore.innerText = `${data.high_score}`
        userLatest.innerText = `${data.last_score}`
        userAverage.innerText = `${data.average_score}`
        userLowest.innerText = `${data.lowest_score}`
        userCreation.innerText = `${formattedCreationDate}`
        userGames.innerText = `${data.games_played}`
        userPosition.innerText = `${data.user_position}`
        refresh.style.display = "block"
      });
  });
});
