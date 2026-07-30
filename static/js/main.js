// INTERPRETA+ - interações do front-end

document.addEventListener("DOMContentLoaded", () => {
    // Destaca a alternativa selecionada
    document.querySelectorAll(".alternativa input[type='radio']").forEach((input) => {
        input.addEventListener("change", () => {
            const grupo = document.getElementsByName(input.name);
            grupo.forEach((r) => r.closest(".alternativa").classList.remove("selecionada"));
            input.closest(".alternativa").classList.add("selecionada");
        });
    });

    // Efeito simples de "pop" ao clicar em botões grandes
    document.querySelectorAll(".botao-grande").forEach((botao) => {
        botao.addEventListener("click", () => {
            botao.style.transform = "scale(0.97)";
            setTimeout(() => (botao.style.transform = ""), 100);
        });
    });

    // Marca visualmente linhas corretas/erradas na tela de resultado (reforço)
    document.querySelectorAll(".linha-detalhe.correta").forEach((linha) => {
        linha.style.animation = "aparecer 0.3s ease-in";
    });
});
