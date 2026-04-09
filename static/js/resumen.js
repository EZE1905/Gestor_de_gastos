let labels_gastos = Object.keys(window.datos)
let data_gastos = Object.values(window.datos)

let grafico_gastos = document.getElementById("gastos").getContext("2d");
let migrafico = new Chart(grafico_gastos,{
    type:"bar",
    data:{
        labels: labels_gastos,
        datasets: [{
            label: "gastos",
            data: data_gastos
        }]
    }
})