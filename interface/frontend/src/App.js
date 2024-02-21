import './App.css';
import axios from 'axios';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';

// Importing components
import NavbarMenu from './components/Navbar/NavbarMenu';
import Testing from './components/Testing/Testing';
import Settings from './components/Settings/Settings';

function App() {
  return (
     <Router>
      <div className="App" style={{margin: 0, padding: 0 }}>
        <NavbarMenu />
        <Routes>
            <Route path="/" exact element={<Testing />} />
            <Route path={"/settings"} element={<Settings />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
