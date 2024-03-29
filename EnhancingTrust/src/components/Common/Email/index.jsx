import { useState } from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import TemplateRenderer from '../TemplateRenderer';
import EmailHeader from './EmailHeader';
import { Events } from '../../../constants';
import Overlay from '../Overlay';
import { toast } from 'react-toastify';



const Email = (props) => {
  const [config, setConfig] = useState();
  const { logEvent } = props;
  const [showOverlay, setShowOverlay] = useState(false);


  const eventHandler = (e, event, attribs, metadata) => {
    if (typeof attribs?.['data-default'] === 'undefined') {
      e.preventDefault();
      e.stopPropagation();
    }

    logEvent(event, metadata);
  };

  const onLinkClick = (...params) => {
    eventHandler(...params);
    toast.info("All links have been disabled in this study", {
      onClose: () => setShowOverlay(false),
      onOpen: () => setShowOverlay(true),
    });
    toast.clearWaitingQueue();
  }


  return (
    <Container fluid className="p-0">
      {showOverlay && <Overlay onClick={() => toast.dismiss()} />}
      <Row className="et-email gx-0">
        <Col xs="auto" className="d-md-flex d-none">
          <div className="et-email__menu-side bg-light px-3">
            <Button variant="link" className="py-3 et-email__icon-btn" onClick={(e) => onLinkClick(e, Events.EMAIL_INBOX)}>
              <i className="et-tray" />
            </Button>
            <Button variant="link" className="py-3 et-email__icon-btn" onClick={(e) => onLinkClick(e, Events.EMAIL_FAVORITES)}>
              <i className="et-star" />
            </Button>
            <Button variant="link" className="py-3 et-email__icon-btn" onClick={(e) => onLinkClick(e, Events.EMAIL_DRAFTS)}>
              <i className="et-pen" />
            </Button>
            <Button variant="link" className="py-3 et-email__icon-btn" onClick={(e) => onLinkClick(e, Events.EMAIL_SPAM)}>
              <i className="et-info-octa" />
            </Button>
          </div>
        </Col>
        <Col>
          <div>
            <div className="et-email__menu-top px-lg-7 px-md-5 px-3 py-3 justify-content-between">
              <div className="d-flex">
                <Button variant="link" className="et-email__menu-top__item et-email__icon-btn" onClick={(e) => onLinkClick(e, Events.EMAIL_BACK)}>
                  <i className="et-arrow-left" />
                </Button>
                <Button variant="link" className="et-email__menu-top__item et-email__icon-btn" onClick={(e) => onLinkClick(e, Events.EMAIL_ARCHIVE)}>
                  <i className="et-archive" />
                  <span className="d-sm-block d-none">Archive</span>
                </Button>
                <Button variant="link" className="et-email__menu-top__item et-email__icon-btn" onClick={(e) => onLinkClick(e, Events.EMAIL_REPORT_SPAM)}>
                  <i className="et-forbiden" />
                  <span className="d-sm-block d-none">Report Spam</span>
                </Button>
                <Button variant="link" className="et-email__menu-top__item et-email__icon-btn" onClick={(e) => onLinkClick(e, Events.EMAIL_DELETE)}>
                  <i className="et-trash" />
                  <span className="d-sm-block d-none">Delete</span>
                </Button>
              </div>
              <Button variant="link" className="et-email__menu-top__dots et-email__icon-btn" onClick={(e) => onLinkClick(e, Events.EMAIL_DOT_MENU)}>
                <i className="et-dots" />
              </Button>
            </div>
            <div className="px-lg-7 px-md-5 px-3 pt-3">
              <EmailHeader logEvent={props.logEvent} config={config} showTooltips={props.showTooltips} />
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
