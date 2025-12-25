const machines = {{ machines| tojson }};

function calculateRemainingLifespan(purchaseDate, lifespanYears) {
    return 50; // Set all progress bars to 50%
}

function showMachineDetails(index) {
    const details = document.getElementById("machineDetails");
    const machine = machines[index];
    let html = `<h3>${machine.name}</h3>`;
    html += `<img src="${machine.image}" alt="${machine.name}">`;
    html += `<p>Purchased on: ${machine.purchaseDate}</p>`;
    html += `<p>Lifespan: ${machine.lifespan} years</p>`;
    const lifespanPercentage = calculateRemainingLifespan(machine.purchaseDate, machine.lifespan);
    html += `<div class="progress-container">
                <div class="progress-bar" style="width:${lifespanPercentage}%">${Math.round(lifespanPercentage)}%</div>
            </div>`;
    html += `<h4>Parts:</h4>`;
    html += `<ul>`;
    machine.parts.forEach(part => {
        const partLifespanPercentage = calculateRemainingLifespan(part.purchaseDate, part.lifespan);
        html += `<li>${part.name} - Purchased: ${part.purchaseDate}, Lifespan: ${part.lifespan} years
                    <div class="progress-container">
                        <div class="progress-bar" style="width:${partLifespanPercentage}%">${Math.round(partLifespanPercentage)}%</div>
                    </div>
                </li>`;
    });
    html += `</ul>`;
    details.innerHTML = html;
}