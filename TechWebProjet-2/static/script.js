// Acceder au elements HTML
const title = document.getElementById('title');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const calenderBloc = document.getElementById('calenderBloc');

var currDate = new Date();

// Fonction main qui serra appelé quand le DOM est prêt
function main(){
    // Appele la fonction buildCalender pour crée le calendrier
    buildCalender(currDate);

    // Fonction pour changer le mois, -1 pour le mois d'avant et +1 pour le mois d'après
    // La fonction changeMonth(value) est appelé lorque les buttons indiquer sont clicker
    prevBtn.addEventListener('click', function(){changeMonth(-1)});
    nextBtn.addEventListener('click', function(){changeMonth(1)});
}

// Fonction pour crée le calendrier
function buildCalender(date){
    // Get le mois et l'année actuelle
    const currMonth = date.getMonth();
    const currYear = date.getFullYear();

    //  Get le jour actuel et le dernier date
    const firstDay = new Date(currYear, currMonth, 0).getDay();
    const lastDate = new Date(currYear, currMonth + 1, 0).getDate();

    // liste avec les mois en String
    var months = ['January', 'February', 'March', 'April', 'May', 'June','July', 'August', 'September', 'October', 'November', 'December'];

    // Changer le content du element HTML title, on mets le mois actuel et l'année actuelle
    title.textContent = `${months[currMonth]} ${currYear}`
    // supprimer le innerHTML de l'élément calenderBloc
    calenderBloc.innerHTML = '';

    // Creation d'une ligne de table en HTML et y mettre les jours
    var dateRow = document.createElement('tr');
    for (let i = 0; i < firstDay; i++) {
        const emptyCell = document.createElement('td');
        dateRow.appendChild(emptyCell);
    }

    // Crée et passer à la ligne suivante quand on arrive a dimanche(7)
    for (let day = 1; day <= lastDate; day++) {
        if (dateRow.children.length === 7) {
            calenderBloc.appendChild(dateRow);
            dateRow = document.createElement('tr');
        }
        const dateCell = document.createElement('td');
        dateCell.textContent = day;
        dateRow.appendChild(dateCell);
    }

    // ajouter la table crée au calenderBloc
    if (dateRow.children.length > 0) {
        calenderBloc.appendChild(dateRow);
    }
}

// Fonction pour changer le mois +1 ou -1
function changeMonth(value){
    currDate.setMonth(currDate.getMonth() + value);
    buildCalender(currDate);
}

// Appeler la fonction main() quand DOM est prêt
document.addEventListener('DOMContentLoaded', main());