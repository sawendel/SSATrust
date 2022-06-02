import React from 'react';
import { ToastContainer, Zoom } from 'react-toastify';
import {
  BrowserRouter,
  Routes,
  Route,
} from 'react-router-dom';
import HomePage from './components/HomePage';
import ModeWrapper from './components/ModeWrapper';
import Layout from './components/Common/Layout';

const App = () => (
  <>
    <ToastContainer
      position="top-center"
      theme="colored"
      transition={Zoom}
      limit={1}
      autoClose={5000}
      hideProgressBar={false}
      newestOnTop={false}
      closeOnClick
      rtl={false}
      pauseOnFocusLoss
    />
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout id={1} />}>
          <Route path="/" index exact element={<HomePage id={1} />} />
          <Route path="/workflow/:id" element={<ModeWrapper />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </>
);

export default App;
