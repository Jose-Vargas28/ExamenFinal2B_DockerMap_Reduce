package com.poweresfot.demo.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import com.poweresfot.demo.model.Interaccion;
import com.poweresfot.demo.repository.InteraccionRepository;

@RestController
public class DatosController {

    @Autowired
    private InteraccionRepository repository;

    @Value("${servidor.nombre}")
    private String servidorNombre;


    @GetMapping(value = "/datos", produces = MediaType.TEXT_PLAIN_VALUE)
    public ResponseEntity<String> obtenerDatos() {
        List<Interaccion> lista = repository.findAll();

        StringBuilder sb = new StringBuilder();
        sb.append("=== Respondido por: ").append(servidorNombre).append(" ===\n");

        for (Interaccion i : lista) {
            sb.append(i.getUsuario()).append(", ")
              .append(i.getAccion()).append(", ")
              .append(i.getFecha()).append(", ")
              .append(i.getHora()).append(", ")
              .append(i.getShortVideo())
              .append("\n");
        }

        return ResponseEntity.ok()
                .header("X-Servidor", servidorNombre)
                .body(sb.toString());
    }

    @GetMapping(value = "/servidor", produces = MediaType.TEXT_PLAIN_VALUE)
    public String servidor() {
        return "Respondio: " + servidorNombre;
    }
}