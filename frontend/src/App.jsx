import React, { Component } from 'react';
import axios from 'axios';
import {
  Section,
  Heading,
  Button,
  Hero,
  Container,
} from 'react-bulma-components';
import socketIOClient from 'socket.io-client';
import './App.css';

const API_URL = 'http://127.0.0.1:5000';
const SOCKETIO_URI = API_URL + '/messages';

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      messages: [],
      requestSid: '',
      placeholder: 'Output from the server',
    };
  }
  appendWithDatetime = (message) => `[${new Date().toISOString()}] ${message}`;

  componentDidMount() {
    const socket = socketIOClient(SOCKETIO_URI);
    socket.on('connect', function () {
      socket.emit('connection', { message: 'SocketIO client connected' });
    });
    socket.on('confirmation', (data) => {
      this.setState({
        messages: [
          ...this.state.messages,
          this.appendWithDatetime(data.message),
        ],
        requestSid: data.requestSid,
      });
    });
    socket.on('response', (data) => {
      this.setState({
        messages: [
          ...this.state.messages,
          this.appendWithDatetime(data.message),
        ],
        loading: false,
      });
    });
  }

  clearMessages = () => {
    this.setState({
      messages: [],
      placeholder: 'Messages cleared',
    });
  };

  onTaskStart = () => {
    this.setState({ loading: true });
    const { requestSid } = this.state;
    axios
      .post(API_URL + '/start_task', { requestSid }, { timeout: 5000 })
      .then((response) => {
        this.setState({
          messages: [
            ...this.state.messages,
            this.appendWithDatetime(response.data.message),
          ],
        });
      })
      .catch((error) => {
        this.setState({ loading: false });
        if (error.code === 'ECONNABORTED') {
          this.setState({
            messages: [
              ...this.state.messages,
              this.appendWithDatetime('Connection timed out'),
            ],
          });
        } else {
          this.setState({
            messages: [
              ...this.state.messages,
              this.appendWithDatetime(error.message),
            ],
          });
        }
      });
  };

  render() {
    const { loading, messages, placeholder } = this.state;
    const startButtonClass = 'is-primary ' + (loading && 'is-loading');
    return (
      <Container fluid className="App">
        <Hero>
          <Hero.Body>
            <Heading className="has-text-light">
              Flask asynchronous example
            </Heading>
            <Heading className="has-text-grey-lighter" subtitle size={6}>
              Example of live communication between Flask/SocketIO application,
              Celery and ReactJS frontend
            </Heading>
          </Hero.Body>
        </Hero>
        <Section>
          <textarea
            className="textarea"
            placeholder={placeholder}
            rows="10"
            value={messages.join('\n')}
            readOnly={true}
          ></textarea>
          <div className="mt-5">
            <Button className={startButtonClass} onClick={this.onTaskStart}>
              Click here to start your async task
            </Button>
            <Button className="ml-2" onClick={this.clearMessages}>
              Clear messages
            </Button>
          </div>
        </Section>
      </Container>
    );
  }
}
