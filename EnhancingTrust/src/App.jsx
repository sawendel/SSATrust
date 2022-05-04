import React from 'react';
import {
  BrowserRouter,
  Routes,
  Route,
} from 'react-router-dom';
import HomePage from './components/HomePage';
import ModeWrapper from './components/ModeWrapper';
import Layout from './components/Common/Layout';

const App = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Layout id={1} />}>
        <Route path="/" index exact element={<HomePage id={1} />} />
        <Route path="/workflow/:id" element={<ModeWrapper />} />
      </Route>
    </Routes>
  </BrowserRouter>
);

export default App;
