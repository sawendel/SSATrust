import { useState } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import TemplateRenderer from '../TemplateRenderer';
import EmailHeader from './EmailHeader';

const Email = (props) => {
  const [config, setConfig] = useState();

  return (
    <Container fluid className="p-0">
      <Row className="et-email gx-0">
        <Col xs="auto" className="d-md-flex d-none">
          <div className="et-email__menu-side bg-light px-3">
            <i className="py-3 et-tray" />
            <i className="py-3 et-star" />
            <i className="py-3 et-pen" />
            <i className="py-3 et-info-octa" />
          </div>
        </Col>
        <Col>
          <div>
            <div className="et-email__menu-top px-lg-7 px-md-5 px-3 py-3 justify-content-between">
              <div className="d-flex">
                <i className="et-email__menu-top__item et-arrow-left" />
                <div className="et-email__menu-top__item">
                  <i className="et-archive" />
                  <span className="d-sm-block d-none">Archive</span>
                </div>
                <div className="et-email__menu-top__item">
                  <i className="et-forbiden" />
                  <span className="d-sm-block d-none">Report Spam</span>
                </div>
                <div className="et-email__menu-top__item">
                  <i className="et-trash" />
                  <span className="d-sm-block d-none">Delete</span>
                </div>
              </div>
              <i className="et-dots et-email__menu-top__dots" />
            </div>
            <div className="px-lg-7 px-md-5 px-3 pt-3">
              <EmailHeader config={config} />
              <TemplateRenderer {...props} setOptions={setConfig} />
            </div>
          </div>
        </Col>
      </Row>
    </Container>
  );
};

Email.defaultProps = {
  templateUrl: 'design.html',
};

export default Email;
