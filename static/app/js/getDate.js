
function getFutureDates() {
    const today = new Date();
    const futureDates = [];

    for (let i = 0; i < 7; i++) {
        const date = new Date();
        date.setDate(today.getDate() + i);
        const dateString = formatDate(date);
        const dayOfWeek = getDayOfWeek(date);
        futureDates.push({ date: dateString, dayOfWeek: dayOfWeek });
    }

    return futureDates;
}

function formatDate(date) {
    return date.getDate();
}

function getDayOfWeek(date) {
    const daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    return daysOfWeek[date.getDay()];
}

