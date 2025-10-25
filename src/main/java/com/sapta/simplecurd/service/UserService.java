package com.sapta.simplecurd.service;

import com.sapta.simplecurd.entity.User;
import com.sapta.simplecurd.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.Optional;

@Service
public class UserService {

  @Autowired
  private UserRepository userRepository;

  public List<User> getAllUsers() {
    return userRepository.findAll();
  }

  public Optional<User> getUserById(Long id) {
    return userRepository.findById(id);
  }

  public User createUser(User user) {
    if (userRepository.existsByEmail(user.getEmail())) {
      throw new ResponseStatusException(HttpStatus.CONFLICT, "User with email " + user.getEmail() + " already exists");
    }
    return userRepository.save(user);
  }

  public User updateUser(Long id, User userDetails) {
    User user = userRepository.findById(id)
        .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "User not found with id: " + id));

    if (!user.getEmail().equals(userDetails.getEmail()) &&
        userRepository.existsByEmail(userDetails.getEmail())) {
      throw new ResponseStatusException(HttpStatus.CONFLICT,
          "User with email " + userDetails.getEmail() + " already exists");
    }

    user.setName(userDetails.getName());
    user.setEmail(userDetails.getEmail());
    user.setAddress(userDetails.getAddress());

    return userRepository.save(user);
  }

  public void deleteUser(Long id) {
    User user = userRepository.findById(id)
        .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "User not found with id: " + id));
    userRepository.delete(user);
  }
}