import React, { Component } from "react";
import axios from "axios";
import { Button, Tag, Heading } from "react-bulma-components";
import socketIOClient from "socket.io-client";
import './App.css';

const API_URL = 'http://127.0.0.1:5000'
const SOCKETIO_URI = API_URL + '/sio'

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      message: '',
      requestSid: "",
      connectionStatus: "",
      response: ""
    };
  }

  componentDidMount() {
    const socket = socketIOClient(SOCKETIO_URI);
    console.log(socket);
    socket.on("connect", function () {
      socket.emit('connection', { message: 'SocketIO client connected' })
    });
    socket.on('confirmation', data => {
      console.log(data);
      this.setState({ ...data })
    });
    socket.on('response', data => {
      console.log(data);
      this.setState({ ...data, loading: false })
    })
  }


  onClickHandler = () => {
    this.setState({ loading: true });
    const { requestSid } = this.state
    axios
      .post(API_URL + "/start_task", { requestSid })
      .then((response) => {
        console.log(response.data);
        this.setState({ ...response.data });
      })
      .catch((err) => {
        this.setState({ loading: false })
        console.error(err)
      });
  };
  render() {
    const { connectionStatus, loading, message } = this.state;
    return (
      <div className="App">
        <header className="App-header">
          <Button
            className={"is-primary " + (loading && "is-loading")}
            onClick={this.onClickHandler}
          >
            Click here to start your async task
          </Button>
          {connectionStatus && (
            <Heading subtitle={true} className="has-text-white">
              <Tag>{connectionStatus}</Tag>
            </Heading>)}
          {message && (
            <Heading subtitle={true} className="has-text-white">
              <Tag>{message}</Tag>
            </Heading>
          )}
        </header>
      </div>
    );
  }
}
