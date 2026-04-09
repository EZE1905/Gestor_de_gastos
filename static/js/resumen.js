let labels_gastos = Object.keys(window.datos_gastos)
let data_gastos = Object.values(window.datos_gastos)

let grafico_gastos = document.getElementById("gastos").getContext("2d");
let migrafico = new Chart(grafico_gastos,{
    type:"bar",
    data:{
        labels: labels_gastos,
        datasets: [{
            label: "gastos",
            data: data_gastos,
            backgroundColor:[
                "#E57373"
            ]
        }]
    }
})

let labels_ingresos =  Object.keys(window.datos_ingresos)
let data_ingresos =  Object.values(window.datos_ingresos)

let grafico_ingresos = document.getElementById("ingresos").getContext("2d")
let chart_ingresos = new Chart(grafico_ingresos,{
    type: "bar",
    data:{
        labels: labels_ingresos,
        datasets:[{
            label: "ingresos",
            data: data_ingresos,
            backgroundColor:[
                "#81C784"
            ]
        }]
    }
})

let labels_totales = Object.keys(window.datos_totales)
let data_totales = Object.values(window.datos_totales)

let grafico_balance = document.getElementById("balance").getContext("2d")
let chart_balance = new Chart(grafico_balance,{
    type: "pie",
    data:{
        labels: labels_totales,
        datasets:[{
            label: "balance",
            data: data_totales,
            backgroundColor:[
                "#E57373",
                "#81C784",
                "#64B5F6"
            ],
            hoverOffset: 4
        }],
    }
})