"use strict";

function format2(x) {
    return (x < 10 ? "0" + x : x.toString());
}

$("#form").validate({
    rules: {
        data_inicial: { required: true },
        data_final: { required: true }
    },
    submitHandler: function () {
        atualizarDados();
    }
});

function gerarGraficoUsoMedioZona(dados) {
    let div = document.getElementById("div-grafico-uso-medio-zona");
    div.innerHTML = '<canvas id="grafico-uso-medio-zona" style="height: 35vh;"></canvas>';

    let labels = [];
    let data = [];

    for (let i = 0; i < dados.length; i++) {
        labels.push("Zona " + dados[i].zona);
        data.push(dados[i].soma_media);
    }

    new Chart(document.getElementById("grafico-uso-medio-zona"), {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Média de Uso nos Dias do Intervalo",
                backgroundColor: "#1cc88a",
                borderColor: "#1cc88a",
                data: data,
            }],
        },
        options: {
            maintainAspectRatio: false,
            scales: {
                x: {
                    maxBarThickness: 40,
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                legend: { display: true }
            }
        }
    });
}

function gerarGraficoUsoMedioHora(dados) {
    let div = document.getElementById("div-grafico-uso-medio-hora");
    div.innerHTML = '<canvas id="grafico-uso-medio-hora" style="height: 35vh;"></canvas>';

    let labels = [];
    let data = [];

    for (let item in dados) {
        labels.push(item + ":00");
        data.push(dados[item]);
    }

    new Chart(document.getElementById("grafico-uso-medio-hora"), {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Média do Pico de Pessoas no Intervalo",
                backgroundColor: "#ffc900",
                borderColor: "#ffc900",
                data: data,
            }],
        },
        options: {
            maintainAspectRatio: false,
            scales: {
                x: {
                    maxBarThickness: 40,
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                legend: { display: true }
            }
        }
    });
}

function gerarGraficoConsolidadoDiaMes(dados) {
    let div = document.getElementById("div-grafico-consolidado-dia-mes");
    div.innerHTML = '<canvas id="grafico-consolidado-dia-mes" style="height: 35vh;"></canvas>';

    let labels = [], data = [];

    for (let i = 0; i < dados.length; i++) {
        labels.push(dados[i].dia);
        data.push(dados[i].entrada);
    }

    new Chart(document.getElementById("grafico-consolidado-dia-mes"), {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Entrada Total",
                backgroundColor: "#4e73df",
                hoverBackgroundColor: "#2e59d9",
                borderColor: "#4e73df",
                data: data,
            }],
        },
        options: {
            maintainAspectRatio: false,
            layout: {
                padding: {
                    left: 10,
                    right: 25,
                    top: 25,
                    bottom: 0
                }
            },
            scales: {
                x: {
                    gridLines: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        maxTicksLimit: 10
                    },
                    maxBarThickness: 25,
                },
                y: {
                    //display: false,
                    ticks: {
                        min: 0,
                        max: 10,
                        maxTicksLimit: 10,
                        padding: 10
                    },
                    gridLines: {
                        color: "rgb(234, 236, 244)",
                        zeroLineColor: "rgb(234, 236, 244)",
                        drawBorder: false,
                        borderDash: [2],
                        zeroLineBorderDash: [2]
                    }
                },
            },
            legend: {
                display: false
            },
            tooltips: {
                titleMarginBottom: 10,
                titleFontColor: '#6e707e',
                titleFontSize: 14,
                backgroundColor: "rgb(255,255,255)",
                bodyFontColor: "#858796",
                borderColor: '#dddfeb',
                borderWidth: 1,
                xPadding: 15,
                yPadding: 15,
                displayColors: false,
                caretPadding: 10
            },
        }
    });
}

async function atualizarDados() {
    waitSwal();

    try {
        let data_inicial = document.getElementById("data_inicial").value;
        let data_final = document.getElementById("data_final").value;

        let response = await fetch(`/obterDadosConsolidadoDiaMes?data_inicial=${data_inicial}&data_final=${data_final}`);
        let respZona = await fetch(`/obterUsoMedioZona?data_inicial=${data_inicial}&data_final=${data_final}`);
        let respHora = await fetch(`/obterUsoMedioHora?data_inicial=${data_inicial}&data_final=${data_final}`);

        if (response.ok && respZona.ok && respHora.ok) {
            Swal.close();

            const obj = await response.json();
            const objZona = await respZona.json();
            const objHora = await respHora.json();

            if (!obj || !obj.consolidadoDiaMes || !obj.consolidadoDiaMes.length) {
                Swal.fire("Erro", "Sem dados no período especificado!", "error");
                return;
            }
            
            // Atualizando Grandes Números

            let totalVisitas = 0;
            if (obj && obj.consolidadoDiaMes) {
                for (let i = 0; i < obj.consolidadoDiaMes.length; i++) {
                    totalVisitas += obj.consolidadoDiaMes[i].entrada || 0;
                }
            }
            document.getElementById("big-total-visitas").innerText = totalVisitas;

            let zonaMaisMovimentada = "-";
            if (objZona && objZona.uso_medio_zona && objZona.uso_medio_zona.length) {
                let maxZona = objZona.uso_medio_zona[0];
                for (let i = 1; i < objZona.uso_medio_zona.length; i++) {
                    if (objZona.uso_medio_zona[i].soma_media > maxZona.soma_media) {
                        maxZona = objZona.uso_medio_zona[i];
                    }
                }
                zonaMaisMovimentada = "Zona " + maxZona.zona;
            }
            document.getElementById("big-zona-mais-movimentada").innerText = zonaMaisMovimentada;

            let horarioPico = "-";
            if (objHora && objHora.uso_medio_hora) {
                let max = -1, maxHora = "";
                for (let hora in objHora.uso_medio_hora) {
                    if (objHora.uso_medio_hora[hora] > max) {
                        max = objHora.uso_medio_hora[hora];
                        maxHora = hora;
                    }
                }
                if (maxHora !== "") {
                    horarioPico = maxHora + "h";
                }
            }
            document.getElementById("big-horario-pico").innerText = horarioPico;

            // Gerando Gráficos

            gerarGraficoConsolidadoDiaMes(obj.consolidadoDiaMes);
            gerarGraficoUsoMedioZona(objZona.uso_medio_zona);
            gerarGraficoUsoMedioHora(objHora.uso_medio_hora)
        } else {
            await exibirErro(respHora);
        }
    } catch (ex) {
        Swal.fire("Erro", "Erro ao listar os dados: " + ex.message, "error");
    }
}

atualizarDados();