package com.poweresfot.demo.model;

import java.time.LocalDate;
import java.time.LocalTime;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "redes")
public class Interaccion {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private String usuario;

    // Columna "accion" en la BD (antes se llamaba tipo_interaccion)
    private String accion;

    private LocalDate fecha;

    private LocalTime hora;


    @Column(name = "short")
    private String shortVideo;

    public Interaccion() {}

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public String getUsuario() { return usuario; }
    public void setUsuario(String usuario) { this.usuario = usuario; }

    public String getAccion() { return accion; }
    public void setAccion(String accion) { this.accion = accion; }

    public LocalDate getFecha() { return fecha; }
    public void setFecha(LocalDate fecha) { this.fecha = fecha; }

    public LocalTime getHora() { return hora; }
    public void setHora(LocalTime hora) { this.hora = hora; }

    public String getShortVideo() { return shortVideo; }
    public void setShortVideo(String shortVideo) { this.shortVideo = shortVideo; }
}
