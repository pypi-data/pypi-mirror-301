import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"

interface State {
  numClicks: number
  isFocused: boolean
  clickedIndex: number | null // Track the index of the clicked item
}

class MyComponent extends StreamlitComponentBase<State> {
  public state = { numClicks: 0, isFocused: false, clickedIndex: null } // Initialize clickedIndex

  public render = (): ReactNode => {
    const items = this.props.args["items"] || []
    const title = this.props.args["title"] || "Chat history"; // Added title variable

    // Ensure items is an array
    if (!Array.isArray(items)) {
      return (
        <div>
          <p>No items available.</p>
        </div>
      )
    }

    // Show a list of item items as clickable buttons
    return (
      <div>
        {/* Use the title variable instead of hardcoded text */}
        <p style={{ fontWeight: 'bold' }}>{title}</p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
          {items.map((item: string, index: number) => ( // Changed item type to string
            <button
              key={index}
              onClick={() => this.onItemClicked(item, index)} // Pass item directly
              style={{
                padding: '8px 12px', // Smaller padding
                cursor: 'pointer',
                border: 'none', // No border
                outline: 'none', // Remove blue border when clicked
                borderRadius: '5px',
                backgroundColor: this.state.clickedIndex === index ? '#d0d0d0' : '#F0F2F6', // Change color if clicked
                transition: 'background-color 0.3s', // Smooth transition for hover effect
                fontSize: '14px', // Smaller font size
                textAlign: 'left', // Align text to the left
                width: '100%', // Make button take full width
                display: 'flex', // Use flexbox for alignment
                justifyContent: 'flex-start', // Align text to the left
              }}
              onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#e0e0e0'} // Hover effect
              onMouseLeave={(e) => {
                if (this.state.clickedIndex !== index) {
                  e.currentTarget.style.backgroundColor = '#F0F2F6'; // Reset background color if not clicked
                }
              }}
            >
              {item}
            </button>
          ))}
        </div>
      </div>
    )
  }

  /** Click handler for item. */
  private onItemClicked = (item: string, index: number): void => {
    // Notify Streamlit of the clicked item.
    Streamlit.setComponentValue(item);
    this.setState({ clickedIndex: index }); // Update clickedIndex state
  }
}


// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(MyComponent)
