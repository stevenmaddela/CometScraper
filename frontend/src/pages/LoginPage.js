import { Box, TextField, Drawer, Button, CssBaseline, Link, Paper, Grid, Typography } from '@mui/material';
import * as React from 'react';
import "./Login.css";
import utdfintechlogo from "../components/utdfintechlogo.png";
import logingraphicblue1 from "../components/logingraphicblue1.png";
import candlestick from "../components/candlestick.png";

import { useHistory } from "react-router-dom";
import { useEffect, useState } from "react";
import {  auth, database, googleAuthProvider , } from "../config/firebase";
import firebase from 'firebase/compat/app';
import { getAuth, sendPasswordResetEmail } from "firebase/auth";
import { InputAdornment } from '@mui/material';


function LoginPage() {
    
    const history = useHistory();
    const [isNewUser, setIsNewUser] = useState(false);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [forgotPasswordEmail, setForgotPasswordEmail] = useState("");
    const handleName = e => {setFirstName(e.target.value);}
    const handleLastName = e => {setLastName(e.target.value);};
    const handlePassword = e => {setPassword(e.target.value);}
    const handleEmail = e => {setEmail(e.target.value);};
    const [loginEmail, setLoginEmail] = useState("");
    const [loginPassword, setLoginPassword] = useState("");
    const handleLoginPassword = e => {setLoginPassword(e.target.value);}
    const handleLoginEmail = e => {setLoginEmail(e.target.value);};
    const handleForgotEmail = e => {setForgotPasswordEmail(e.target.value);};
    const registerNewUser = () => {setIsNewUser((prevState) => !prevState)}
    const [loggedIn, setLoggedIn] = useState(false);
    const [forgotPasswordState, setForgotPasswordState] = useState(false);
    const forgotPassword = () => {setForgotPasswordState((prevState) => !prevState)}
    const [passwordError, setPasswordError] = useState("");
    const [emailError, setEmailError] = useState("");
    const [signUpEmailError, setSignUpEmailError] = useState("");
    const [signUpPasswordError, setSignUpPasswordError] = useState("");
    

    useEffect(() => {
        const unsubscribe = auth.onAuthStateChanged((user) => {
          if (user) {
            setLoggedIn(true);
          } else {
            setLoggedIn(false);
          }
        });
    
        return () => unsubscribe();
      }, []);

      const signIn = async () => {
        try {
          if (!loginPassword) { // Check if loginPassword is empty
            throw new Error("Password must not be empty."); // Throw custom error for empty password
        }

            await auth.signInWithEmailAndPassword(loginEmail, loginPassword);
            history.push(`/search`);
        } catch (err) {
            console.error(err);
            if (err.code === 'auth/invalid-email') {

              setEmailError("Invalid Email");
              setLoginEmail("");
               
            } else if (err.code === 'auth/invalid-login-credentials' || err.code === 'auth/user-not-found') {
                // Update the password error message for invalid login credentials or user not found
                setPasswordError("Incorrect email or password");
                // Clear the password field
                setLoginPassword("");
                
            } 
            else if (err.message === "Password must not be empty.") {
              // Update the password error message for empty password
              setPasswordError("Password must be 6+ characters.");
              // Clear the password field
                setLoginPassword("");
            }

            else if (err.code === 'auth/too-many-requests') {
                // Update the password error message for too many login attempts
                setPasswordError("Too many attempts. Try again later.");
                // Clear the password field
                setLoginPassword("");
            } else {
                // Handle other error cases here
                console.error('SHHHHHHHHHHHHHHHHHH Error:', err.code);
            }
        }
    };
    
      const signUp = async () => {
        try {
          await auth.createUserWithEmailAndPassword(email, password);
          const user = auth.currentUser;
          if (user) {
            const uid = user.uid;
      
            // Write user data to the database
            await database.ref(`users/${uid}`).set({
              email: email,
              firstName: firstName,
              lastName: lastName,
              // Add other user information as needed
            });
      
            // Redirect to the search page
            history.push(`/search`);
          } else {
            console.error('No user signed in');
          }
        } catch (err) {
          console.error(err);
          if (err.code === 'auth/invalid-email' || err.code === 'auth/email-already-in-use') {

            setSignUpEmailError("Invalid Email");
            setEmail("");
             
          } else if (err.code === 'auth/weak-password' || err.code === 'auth/missing-password') {
              // Update the password error message for invalid login credentials or user not found
              setSignUpPasswordError("Password must be 6+ characters.");
              // Clear the password field
              setPassword("");
          } else {
              // Handle other error cases here
              console.error('SHHHHHHHHHHHHHHHHHH Error:', err.code);
          }
        }
      };
    
      const signInWithGoogle = async () => {
        try {
          await auth.signInWithPopup(googleAuthProvider);
          history.push(`/search`);
        } catch (err) {
          console.error(err);
        }
      };
    
      const logOut = async () => {
        try {
          await auth.signOut();
        } catch (err) {
          console.error(err);
        }
      };

      const handleForgotPassword = async () => {

        sendPasswordResetEmail(auth, forgotPasswordEmail)
        .then(() => {
          console.log("email sent")
        })
        .catch((error) => {
          const errorCode = error.code;
          const errorMessage = error.message;
          console.log(errorMessage + " " + errorCode)
        });
      }

      const clearPasswordError = () => {
        setPasswordError("");
    };

     const clearEmailError = () => {
      setEmailError("");
    }

    const clearSignUpEmailError = () => {
      setSignUpEmailError("");
    }

    const clearSignUpPasswordError = () => {
      setSignUpPasswordError("");
    }
    

    return (
        <div style={{ height: '100vh'  }} >
            <Drawer className="custom-grid"
                variant="permanent"
                anchor="left"
                sx={{ }}
                
            >
                <Grid container component="main" className="custom-grid" sx={{ height: '100vh',
                
     }}>
                    <Grid item
                        xs={false}
                        sm={4}
                        md={7}
                        sx={{
                            backgroundSize: 'cover',
                            backgroundPosition: 'center',
                            
                            
                        }}
                    >
                        <Grid item
                            style={{
                                width: "100vw",
                                height: "13vh",
                                display: "flex",
                                flexDirection: "row",
                                paddingLeft:"35px",
                                paddingTop:"35px"
                            }}
                            
                        >
                            <img className="photo" src={utdfintechlogo} style={{width: "62.5px", height: "62.5px"}} />
                            <label className="logoText">
                                Comet
                                <br />
                                Scraper
                            </label>
                            
                        </Grid>
                    
                        <img className="welcomePhoto" src={logingraphicblue1} style={{
                            width: "700px", // Adjust the width as needed
                            height: "auto", // Maintain aspect ratio
                            paddingLeft: "65px", // Adjust left padding as needed
                            paddingTop: "150px", // Adjust top padding as needed
  }}/>
   
                    </Grid>
                    <Grid item xs={12} sm={8} md={5}  elevation={6} square sx={{ }}>
    { !forgotPasswordState? 
    <Box className="infoCard" sx={{ paddingLeft:"75px", textAlign: 'left', paddingBottom: "200px",  }}> {/* Aligning content to the center */}
        <Typography variant="h5" className="loginHeader" style={{fontFamily: 'Avenir',fontWeight : 600,}}>
            Welcome Back,
        </Typography>
        <Typography className="lowerLoginHeader" style={{ fontFamily: 'Avenir' }}>
            {isNewUser ? 'Sign Up' : 'Sign in'}
        </Typography>
        {isNewUser ? (
                                <Box component="form" noValidate sx={{ mt: 1 }}>
                                    <TextField
                                        value={email}
                                        className={"textField customTextField"}
                                        margin="normal"
                                        required={false}
                                        id="email"
                                        label={signUpEmailError ? <span style={{ color: "red" }}>{signUpEmailError}</span> : "EMAIL ADDRESS"} // Set label conditionally
                                        name="email"
                                        autoComplete="email"
                                        autoFocus
                                        onChange={handleEmail}
                                        onFocus={clearSignUpEmailError} // Clear password error when input is focused
                                        InputProps={{
                                            style: {
                                              borderRadius: "7.5px",
                                            }
                                          }}


                                    />
                                    <br />
                                    <TextField
                                        value={password}
                                        className={"textField"}
                                        margin="normal"
                                        required={false}
                                        name="password"
                                        label={signUpPasswordError ? <span style={{ color: "red" }}>{signUpPasswordError}</span> : "PASSWORD"} // Set label conditionally
                                        type="password"
                                        id="password"
                                        autoComplete="current-password"
                                        onChange={handlePassword}
                                        onFocus={clearSignUpPasswordError} // Clear password error when input is focused
                                        InputProps={{
                                            style: {
                                              borderRadius: "7.5px",
                                            }
                                          }}

                                    />
                                    <br />
                                    <TextField
                                        className={"textField"}
                                        margin="normal"
                                        required = {false}
                                        id="first_name"
                                        label={<span style={{ fontFamily: 'Avenir' }}>FIRST NAME</span>}
                                        name="First_Name"
                                        autoComplete="First Name"
                                        onChange={handleName}
                                        InputProps={{
                                            style: {
                                              borderRadius: "7.5px",
                                            }
                                          }}
                                    />
                                    <br />
                                    <TextField
                                        className={"textField"}
                                        margin="normal"
                                        required={false}
                                        name="Last_Name"
                                        label={<span style={{ fontFamily: 'Avenir' }}>LAST NAME</span>}
                                        id="last_name"
                                        autoComplete="Last Name"
                                        onChange={handleLastName}
                                        InputProps={{
                                            style: {
                                              borderRadius: "7.5px",
                                            }
                                          }}
                                    />
                                    <br />
                                    <Button
                                        variant="contained"
                                        sx={{ mt: 3, mb: 2, fontFamily: 'Avenir' }}
                                        onClick={() => {
                                            signUp();                                     
                                        }}
                                    >
                                        Create Account
                                    </Button>
                                    <div
                                        style={{
                                            display: 'flex',
                                            flexDirection: 'row',
                                            alignItems: 'center',
                                        }}
                                    >
                                        <Typography variant="subtitle1" style={{fontFamily: 'Avenir'}}>
                                            Already have an account?
                                        </Typography>
                                        <Button
                                            variant="text"
                                            sx={{ textTransform: 'none' }}
                                            onClick={registerNewUser}
                                        >
                                            <Typography variant="subtitle1" style={{fontFamily: 'Avenir'}}>
                                                Sign In
                                            </Typography>
                                        </Button>
                                    </div>
                                </Box>
                            ) : (
                                <Box component="form" noValidate sx={{ mt: 1 }}>
                                    <TextField
                                        value={loginEmail}
                                        className={"textField"}
                                        margin="normal"
                                        required={false}
                                        id="email"
                                        label={emailError ? <span style={{ color: "red" }}>{emailError}</span> : "EMAIL ADDRESS"} // Set label conditionally
                                        name="email"
                                        autoComplete="email"
                                        autoFocus
                                        onChange={handleLoginEmail}
                                        onFocus={clearEmailError}
                                        InputProps={{
                                            style: {
                                              borderRadius: "7.5px",
                                            }
                                          }}
                                    />
                                    <br />
                                    <TextField
                                      value={loginPassword}
                                      className={"textField"}
                                      margin="normal"
                                      required={false}
                                      name="password"
                                      label={passwordError ? <span style={{ color: "red" }}>{passwordError}</span> : "PASSWORD"} // Set label conditionally
                                      type="password"
                                      id="password"
                                      autoComplete="current-password"
                                      onChange={handleLoginPassword}
                                      onFocus={clearPasswordError} // Clear password error when input is focused
                                  />

                                    <br />
                                    <Button
                                        variant="contained"
                                        sx={{ mt: 3, mb: 2, mr: 5, fontFamily: 'Avenir'}}
                                        onClick={() => {
                                             signIn();
                                        }}
                                    >
                                        Log In
                                    </Button>
                                    
                                    <Button
                                        variant="contained"
                                        className={"googleLoginButton"}
                                        sx={{ mt: 3, mb: 2, fontFamily: 'Avenir'}}
                                        onClick={() => {
                                            signInWithGoogle();
                                        }}
                                    >
                                        Log In With Google
                                    </Button>
                                    <div
                                        style={{
                                            display: 'flex',
                                            flexDirection: 'row',
                                            alignItems: 'center',
                                        }}
                                    >
                                        <Typography variant="subtitle1" style={{fontFamily: 'Avenir'}}> 
                                            Don't have an account?
                                        </Typography>
                                        <Button
                                            variant="text"
                                            sx={{ textTransform: 'none' }}
                                            onClick={registerNewUser}
                                        >
                                            <Typography variant="subtitle1" style={{fontFamily: 'Avenir'}}>
                                                Sign Up
                                            </Typography>
                                        </Button>
                                    </div>
                                    <div>
                                        <Button
                                            variant="text"
                                            sx={{
                                                textTransform: 'none',
                                                padding: 0,
                                            }}
                                        >
                                            <Typography variant="subtitle1" onClick={forgotPassword} style={{fontFamily: 'Avenir'}}>
                                                Forgot your password?
                                            </Typography>
                                        </Button>
                                    </div>
                                </Box>
                            )}
                       
    </Box>
    : 
    <Box className="infoCard" sx={{ paddingLeft:"75px", textAlign: 'left', paddingBottom: "200px",  }}> {/* Aligning content to the center */}
        <Typography variant="h5" className="loginHeader" style={{fontFamily: 'Avenir',fontWeight : 600,}}>
            Forgot Password?
        </Typography>
        <Typography className="lowerLoginHeader" style={{ fontFamily: 'Avenir' }}>
            Send Reset Password Link
        </Typography>
        
                                <Box component="form" noValidate sx={{ mt: 1 }}>
                                    <TextField
                                        value={forgotPasswordEmail}
                                        className={"textField"}
                                        margin="normal"
                                        required={false}
                                        id="email"
                                        label={<span style={{ fontFamily: 'Avenir' }}>EMAIL ADDRESS</span>}
                                        name="email"
                                        autoComplete="email"
                                        autoFocus
                                        onChange={handleForgotEmail}
                                        InputProps={{
                                            style: {
                                              borderRadius: "7.5px",
                                            }
                                          }}
                                    />
                                    <br />
                                    <Button
                                        variant="contained"
                                        sx={{ mt: 3, mb: 2, mr: 5, fontFamily: 'Avenir'}}
                                        onClick={() => {
                                          handleForgotPassword();
                                        }}
                                    >
                                        Email Link
                                    </Button>
                                    
                                    <div
                                        style={{
                                            display: 'flex',
                                            flexDirection: 'row',
                                            alignItems: 'center',
                                        }}
                                    >
                                        <Typography variant="subtitle1" style={{fontFamily: 'Avenir'}}> 
                                            Already have an Account?
                                        </Typography>
                                        <Button
                                            variant="text"
                                            sx={{ textTransform: 'none' }}
                                            onClick={forgotPassword}
                                        >
                                            <Typography variant="subtitle1" style={{fontFamily: 'Avenir'}}>
                                                Sign in
                                            </Typography>
                                        </Button>
                                    </div>
                                  
                                </Box>
                           
    </Box>
    }
</Grid>

                </Grid>
            </Drawer>
        </div>
    );
}
export default LoginPage;
