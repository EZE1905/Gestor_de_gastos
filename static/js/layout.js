let mensajes = window.mensajes
const contenedor = document.getElementById("contenedor_msj")


mensajes.forEach(mensaje => {
            const nuevoDiv = document.createElement("div");
            nuevoDiv.textContent = mensaje[1]
            nuevoDiv.classList.add(mensaje[0])
            contenedor.appendChild(nuevoDiv)
            setTimeout(()=>{
                nuevoDiv.remove()
            },3000)
        })