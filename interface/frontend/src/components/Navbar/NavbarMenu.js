import React from 'react';

import {Navbar, Nav, NavDropdown, NavbarBrand, NavbarToggle, NavbarCollapse} from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
function NavbarMenu() {
   return (
        <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
            <NavbarToggle aria-controls="responsive-NavbarMenu-Nav"/>
            <NavbarCollapse id="responsive-Navbar-Nav">
                <Nav className="mr-auto mx-lg-3">
                    <LinkContainer to='/'>
                        <Nav.Link>Testing</Nav.Link>
                    </LinkContainer>
                    <LinkContainer to='/settings'>
                        <Nav.Link>Settings</Nav.Link>
                    </LinkContainer>
                </Nav>
            </NavbarCollapse>
        </Navbar>
    )
}


export default NavbarMenu;