let mensajes = window.mensajes
const contenedor = document.getElementById("contenedor_msj")


mensajes.forEach(mensaje => {
            const nuevoDiv = document.createElement("div");
            nuevoDiv.textContent = mensaje[1]
            nuevoDiv.classList.add(mensaje[0],"contenedor_msj")
            contenedor.appendChild(nuevoDiv)
            setTimeout(() => {
                nuevoDiv.style.opacity = "0";
                nuevoDiv.style.transform = "translateX(30px)";

                setTimeout(() => {
                    nuevoDiv.remove();
                }, 500);
}, 3000);
        })