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

let meses = {
    "01": "Enero",
    "02": "Febrero",
    "03": "Marzo",
    "04": "Abril",
    "05": "Mayo",
    "06": "Junio",
    "07": "Julio",
    "08": "Agosto",
    "09": "Septiembre",
    "10": "Octubre",
    "11": "Noviembre",
    "12": "Diciembre"
}

let labels_totales_mes = Object.keys(window.datos_ingreso_mes).map(fecha => {
    let partes = fecha.split("-")
    let mes_num = partes[1]
    return meses[mes_num]
})

let data_ingreso_mes = Object.values(window.datos_ingreso_mes)
let data_gasto_mes = Object.values(window.datos_gasto_mes)

let grafico_linea = document.getElementById("evolucion").getContext("2d")
let chart_linea = new Chart(grafico_linea,{
    type:"line",
    data:{
        labels:labels_totales_mes,
        datasets:[{
                label: "Ingresos",
                data: data_ingreso_mes,
                borderColor: "#22c55e",
                backgroundColor: "rgba(34,197,94,0.15)",
                tension: 0.3,
                fill: true,
                pointRadius: 4,
                pointBackgroundColor: "#22c55e"
            },
            {
                label: "Gastos",
                data: data_gasto_mes,
                borderColor: "#ef4444",
                backgroundColor: "rgba(239,68,68,0.15)",
                tension: 0.3,
                fill: true,
                pointRadius: 4,
                pointBackgroundColor: "#ef4444"
            }]
    }
})