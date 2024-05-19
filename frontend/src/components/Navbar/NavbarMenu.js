import React from 'react';

// import {Navbar, Nav, NavbarToggle, NavbarCollapse} from 'react-bootstrap';
// import { LinkContainer } from 'react-router-bootstrap';
function NavbarMenu() {
   return (
       <div className="text-center w-100 bg-dark d-flex align-items-center justify-content-center" style={{ height: '65px' }}>
              <h1 style={{color:"white"}} aria-label='SmartCheck, Application for testing phones'>SmartCheck</h1>
       </div>

        // <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
        //     <NavbarToggle aria-controls="responsive-NavbarMenu-Nav"/>
        //     <NavbarCollapse id="responsive-Navbar-Nav">
        //         <Nav className="mr-auto mx-lg-3 text-center w-100">
        //             {/*<LinkContainer to='/'>*/}
        //             {/*    <Nav.Link>Testing</Nav.Link>*/}
        //             {/*</LinkContainer>*/}
        //             {/*<LinkContainer to='/settings'>*/}
        //             {/*    <Nav.Link>Settings</Nav.Link>*/}
        //             {/*</LinkContainer>*/}
        //         </Nav>
        //     </NavbarCollapse>
        // </Navbar>
    )
}


export default NavbarMenu;