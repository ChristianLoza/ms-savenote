// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Examenes {
    // Mapeo para almacenar las notas de los exámenes por su ID
    mapping(string => string) public notasDeExamenes;

    // Dirección permitida para modificar notas
    address public direccionPermitida = 0xFDF6AE392C4A06C7A29F8340c08a724b484E0477;

    // Modificador que verifica si la cuenta que llama es la permitida
    modifier soloDireccionPermitida() {
        require(msg.sender == direccionPermitida, "Solo la dirección permitida puede llamar a esta función");
        _; // Continuar con la ejecución de la función si la verificación es exitosa
    }

    // Función para guardar la nota del examen
    function guardarNota(string memory idExamen, string memory nota) public soloDireccionPermitida {
        notasDeExamenes[idExamen] = nota;
    }

    // Función para recuperar la nota del examen según su ID
    function obtenerNota(string memory idExamen) public view returns (string memory) {
        return notasDeExamenes[idExamen];
    }

    // Función para actualizar la nota del examen según su ID
    function actualizarNota(string memory idExamen, string memory nuevaNota) public soloDireccionPermitida {
        require(bytes(notasDeExamenes[idExamen]).length != 0, "El ID del examen no existe");
        notasDeExamenes[idExamen] = nuevaNota;
    }
}
