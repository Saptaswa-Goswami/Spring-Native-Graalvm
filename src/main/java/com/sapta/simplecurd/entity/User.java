package com.sapta.simplecurd.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

@Entity
@Table(name = "users")
public class User {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @NotBlank(message = "Name is required")
  @Size(max = 100, message = "Name must not exceed 100 characters")
  @Column(name = "name", nullable = false)
  private String name;

  @NotBlank(message = "Email is required")
  @Email(message = "Email should be valid")
  @Size(max = 150, message = "Email must not exceed 150 characters")
  @Column(name = "email", nullable = false, unique = true)
  private String email;

  @Size(max = 200, message = "Address must not exceed 200 characters")
  @Column(name = "address")
  private String address;

  // Default constructor
  public User() {
  }

  // Constructor with fields
  public User(String name, String email, String address) {
    this.name = name;
    this.email = email;
    this.address = address;
  }

  // Getters and setters
  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getEmail() {
    return email;
  }

  public void setEmail(String email) {
    this.email = email;
  }

  public String getAddress() {
    return address;
  }

  public void setAddress(String address) {
    this.address = address;
  }
}