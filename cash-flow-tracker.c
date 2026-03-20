#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_ENTRIES 1000
#define MAX_DATE_LEN 11
#define MAX_CATEGORY_LEN 50
#define MAX_NOTE_LEN 100

typedef enum {
    INFLOW = 1,
    OUTFLOW = 2
} EntryType;

typedef struct {
    int id;
    char date[MAX_DATE_LEN];           // YYYY-MM-DD
    EntryType type;                    // INFLOW or OUTFLOW
    char category[MAX_CATEGORY_LEN];
    double amount;
    char note[MAX_NOTE_LEN];
    int active;                        // 1 = active, 0 = deleted
} Entry;

static Entry entries[MAX_ENTRIES];
static int entry_count = 0;
static int next_id = 1;
static double opening_cash = 0.0;
static int opening_cash_set = 0;

/* -------------------- Utility Functions -------------------- */

void trim_newline(char *str) {
    if (str == NULL) return;
    size_t len = strlen(str);
    if (len > 0 && str[len - 1] == '\n') {
        str[len - 1] = '\0';
    }
}

void read_line(const char *prompt, char *buffer, size_t size) {
    while (1) {
        printf("%s", prompt);
        if (fgets(buffer, (int)size, stdin) == NULL) {
            clearerr(stdin);
            continue;
        }
        trim_newline(buffer);
        return;
    }
}

int is_blank(const char *s) {
    while (*s) {
        if (!isspace((unsigned char)*s)) return 0;
        s++;
    }
    return 1;
}

int read_int(const char *prompt) {
    char buffer[128];
    char extra;
    int value;

    while (1) {
        read_line(prompt, buffer, sizeof(buffer));

        if (sscanf(buffer, "%d %c", &value, &extra) == 1) {
            return value;
        }

        printf("Invalid number. Try again.\n");
    }
}

double read_double(const char *prompt) {
    char buffer[128];
    char extra;
    double value;

    while (1) {
        read_line(prompt, buffer, sizeof(buffer));

        if (sscanf(buffer, "%lf %c", &value, &extra) == 1) {
            return value;
        }

        printf("Invalid amount. Try again.\n");
    }
}

void read_non_empty_line(const char *prompt, char *buffer, size_t size) {
    while (1) {
        read_line(prompt, buffer, size);
        if (!is_blank(buffer)) return;
        printf("Input cannot be empty. Try again.\n");
    }
}

void pause_for_enter(void) {
    char buffer[8];
    printf("\nPress Enter to continue...");
    fgets(buffer, sizeof(buffer), stdin);
}

const char *type_to_string(EntryType type) {
    return (type == INFLOW) ? "Inflow" : "Outflow";
}

/* -------------------- Core Calculations -------------------- */

double total_inflows(void) {
    double total = 0.0;
    for (int i = 0; i < entry_count; i++) {
        if (entries[i].active && entries[i].type == INFLOW) {
            total += entries[i].amount;
        }
    }
    return total;
}

double total_outflows(void) {
    double total = 0.0;
    for (int i = 0; i < entry_count; i++) {
        if (entries[i].active && entries[i].type == OUTFLOW) {
            total += entries[i].amount;
        }
    }
    return total;
}

double net_cash_flow(void) {
    return total_inflows() - total_outflows();
}

double closing_cash_balance(void) {
    return opening_cash + net_cash_flow();
}

int active_entry_count(void) {
    int count = 0;
    for (int i = 0; i < entry_count; i++) {
        if (entries[i].active) count++;
    }
    return count;
}

/* -------------------- Entry Management -------------------- */

int find_entry_index_by_id(int id) {
    for (int i = 0; i < entry_count; i++) {
        if (entries[i].active && entries[i].id == id) {
            return i;
        }
    }
    return -1;
}

void set_opening_cash(void) {
    opening_cash = read_double("Enter opening cash balance: ");
    opening_cash_set = 1;
    printf("Opening cash set to %.2f\n", opening_cash);
}

void add_entry(EntryType type) {
    if (!opening_cash_set) {
        printf("Please set opening cash first.\n");
        return;
    }

    if (entry_count >= MAX_ENTRIES) {
        printf("Maximum number of entries reached.\n");
        return;
    }

    Entry e;
    e.id = next_id++;
    e.type = type;
    e.active = 1;

    read_non_empty_line("Enter date (YYYY-MM-DD): ", e.date, sizeof(e.date));
    read_non_empty_line("Enter category: ", e.category, sizeof(e.category));

    while (1) {
        e.amount = read_double("Enter amount: ");
        if (e.amount > 0) break;
        printf("Amount must be greater than 0.\n");
    }

    read_line("Enter note (optional): ", e.note, sizeof(e.note));

    entries[entry_count++] = e;

    printf("%s added successfully. ID = %d\n", type_to_string(type), e.id);
}

void print_entries_table_header(void) {
    printf("\n%-5s %-12s %-10s %-20s %-12s %-30s\n",
           "ID", "Date", "Type", "Category", "Amount", "Note");
    printf("-------------------------------------------------------------------------------------------\n");
}

void list_entries(void) {
    if (active_entry_count() == 0) {
        printf("No entries found.\n");
        return;
    }

    print_entries_table_header();

    for (int i = 0; i < entry_count; i++) {
        if (entries[i].active) {
            printf("%-5d %-12s %-10s %-20s %-12.2f %-30s\n",
                   entries[i].id,
                   entries[i].date,
                   type_to_string(entries[i].type),
                   entries[i].category,
                   entries[i].amount,
                   entries[i].note);
        }
    }
}

void list_entries_with_running_balance(void) {
    if (!opening_cash_set) {
        printf("Please set opening cash first.\n");
        return;
    }

    if (active_entry_count() == 0) {
        printf("No entries found.\n");
        return;
    }

    double running_balance = opening_cash;

    printf("\nOpening Cash: %.2f\n", opening_cash);
    printf("\n%-5s %-12s %-10s %-20s %-12s %-15s %-30s\n",
           "ID", "Date", "Type", "Category", "Amount", "Run Balance", "Note");
    printf("--------------------------------------------------------------------------------------------------------\n");

    for (int i = 0; i < entry_count; i++) {
        if (entries[i].active) {
            if (entries[i].type == INFLOW) {
                running_balance += entries[i].amount;
            } else {
                running_balance -= entries[i].amount;
            }

            printf("%-5d %-12s %-10s %-20s %-12.2f %-15.2f %-30s\n",
                   entries[i].id,
                   entries[i].date,
                   type_to_string(entries[i].type),
                   entries[i].category,
                   entries[i].amount,
                   running_balance,
                   entries[i].note);
        }
    }
}

void edit_entry(void) {
    if (active_entry_count() == 0) {
        printf("No entries available to edit.\n");
        return;
    }

    list_entries();

    int id = read_int("\nEnter the ID of the entry to edit: ");
    int index = find_entry_index_by_id(id);

    if (index == -1) {
        printf("Entry not found.\n");
        return;
    }

    Entry *e = &entries[index];
    char buffer[128];

    printf("\nEditing entry ID %d\n", e->id);
    printf("Leave blank to keep current value.\n");

    read_line("New date (current shown below): ", buffer, sizeof(buffer));
    printf("Current date: %s\n", e->date);
    if (!is_blank(buffer)) {
        strncpy(e->date, buffer, sizeof(e->date) - 1);
        e->date[sizeof(e->date) - 1] = '\0';
    }

    read_line("New category (current shown below): ", buffer, sizeof(buffer));
    printf("Current category: %s\n", e->category);
    if (!is_blank(buffer)) {
        strncpy(e->category, buffer, sizeof(e->category) - 1);
        e->category[sizeof(e->category) - 1] = '\0';
    }

    while (1) {
        read_line("New amount (blank to keep current): ", buffer, sizeof(buffer));
        printf("Current amount: %.2f\n", e->amount);

        if (is_blank(buffer)) {
            break;
        }

        char extra;
        double new_amount;
        if (sscanf(buffer, "%lf %c", &new_amount, &extra) == 1 && new_amount > 0) {
            e->amount = new_amount;
            break;
        } else {
            printf("Invalid amount. Try again.\n");
        }
    }

    read_line("New note (blank to keep current): ", buffer, sizeof(buffer));
    printf("Current note: %s\n", e->note);
    if (!is_blank(buffer)) {
        strncpy(e->note, buffer, sizeof(e->note) - 1);
        e->note[sizeof(e->note) - 1] = '\0';
    }

    while (1) {
        read_line("Change type? Enter 1 for Inflow, 2 for Outflow, blank to keep current: ",
                  buffer, sizeof(buffer));
        printf("Current type: %s\n", type_to_string(e->type));

        if (is_blank(buffer)) break;

        int choice;
        char extra;
        if (sscanf(buffer, "%d %c", &choice, &extra) == 1 && (choice == 1 || choice == 2)) {
            e->type = (choice == 1) ? INFLOW : OUTFLOW;
            break;
        } else {
            printf("Invalid type. Try again.\n");
        }
    }

    printf("Entry updated successfully.\n");
}

void delete_entry(void) {
    if (active_entry_count() == 0) {
        printf("No entries available to delete.\n");
        return;
    }

    list_entries();

    int id = read_int("\nEnter the ID of the entry to delete: ");
    int index = find_entry_index_by_id(id);

    if (index == -1) {
        printf("Entry not found.\n");
        return;
    }

    char confirm[8];
    read_line("Are you sure you want to delete this entry? (y/n): ", confirm, sizeof(confirm));

    if (confirm[0] == 'y' || confirm[0] == 'Y') {
        entries[index].active = 0;
        printf("Entry deleted successfully.\n");
    } else {
        printf("Delete cancelled.\n");
    }
}

/* -------------------- Reports -------------------- */

void show_cash_summary(void) {
    if (!opening_cash_set) {
        printf("Please set opening cash first.\n");
        return;
    }

    double inflows = total_inflows();
    double outflows = total_outflows();
    double net = inflows - outflows;
    double closing = opening_cash + net;

    printf("\n=== CASH SUMMARY ===\n");
    printf("Opening Cash   : %.2f\n", opening_cash);
    printf("Total Cash In  : %.2f\n", inflows);
    printf("Total Cash Out : %.2f\n", outflows);
    printf("Net Cash Flow  : %.2f\n", net);
    printf("Closing Cash   : %.2f\n", closing);
    printf("Active Entries : %d\n", active_entry_count());
}

void show_category_summary(void) {
    if (active_entry_count() == 0) {
        printf("No entries found.\n");
        return;
    }

    char categories[MAX_ENTRIES][MAX_CATEGORY_LEN];
    double inflow_totals[MAX_ENTRIES] = {0};
    double outflow_totals[MAX_ENTRIES] = {0};
    int category_count = 0;

    for (int i = 0; i < entry_count; i++) {
        if (!entries[i].active) continue;

        int found = -1;
        for (int j = 0; j < category_count; j++) {
            if (strcmp(categories[j], entries[i].category) == 0) {
                found = j;
                break;
            }
        }

        if (found == -1) {
            strncpy(categories[category_count], entries[i].category, MAX_CATEGORY_LEN - 1);
            categories[category_count][MAX_CATEGORY_LEN - 1] = '\0';
            found = category_count;
            category_count++;
        }

        if (entries[i].type == INFLOW) {
            inflow_totals[found] += entries[i].amount;
        } else {
            outflow_totals[found] += entries[i].amount;
        }
    }

    printf("\n=== CATEGORY SUMMARY ===\n");
    printf("%-20s %-15s %-15s %-15s\n", "Category", "Inflow", "Outflow", "Net");
    printf("-----------------------------------------------------------------\n");

    for (int i = 0; i < category_count; i++) {
        double net = inflow_totals[i] - outflow_totals[i];
        printf("%-20s %-15.2f %-15.2f %-15.2f\n",
               categories[i], inflow_totals[i], outflow_totals[i], net);
    }
}

void forecast_runway(void) {
    if (!opening_cash_set) {
        printf("Please set opening cash first.\n");
        return;
    }

    double current_cash = closing_cash_balance();
    double inflows = total_inflows();
    double outflows = total_outflows();

    if (active_entry_count() == 0) {
        printf("No entries found. Add entries first.\n");
        return;
    }

    int days = read_int("Enter the number of days covered by your current data: ");
    if (days <= 0) {
        printf("Days must be greater than 0.\n");
        return;
    }

    double avg_daily_inflow = inflows / days;
    double avg_daily_outflow = outflows / days;
    double avg_daily_net_burn = (outflows - inflows) / days;

    printf("\n=== RUNWAY FORECAST ===\n");
    printf("Current Cash Balance    : %.2f\n", current_cash);
    printf("Average Daily Inflow    : %.2f\n", avg_daily_inflow);
    printf("Average Daily Outflow   : %.2f\n", avg_daily_outflow);

    if (avg_daily_net_burn > 0) {
        double runway_days = current_cash / avg_daily_net_burn;
        printf("Average Daily Net Burn  : %.2f\n", avg_daily_net_burn);
        printf("Estimated Cash Runway   : %.2f days\n", runway_days);
    } else {
        printf("Average Daily Net Burn  : %.2f\n", avg_daily_net_burn);
        printf("Runway                  : Not limited at current trend\n");
    }
}

/* -------------------- Menu -------------------- */

void show_menu(void) {
    printf("\n================ CASH FLOW TRACKER ================\n");
    printf("1.  Set Opening Cash\n");
    printf("2.  Add Inflow\n");
    printf("3.  Add Outflow\n");
    printf("4.  View All Entries\n");
    printf("5.  View Entries With Running Balance\n");
    printf("6.  Edit Entry\n");
    printf("7.  Delete Entry\n");
    printf("8.  View Cash Summary\n");
    printf("9.  View Category Summary\n");
    printf("10. Forecast Cash Runway\n");
    printf("11. Quit\n");
    printf("===================================================\n");
}

int main(void) {
    int running = 1;

    printf("Welcome to the Cash Flow Tracker\n");

    while (running) {
        show_menu();
        int choice = read_int("Choose an option: ");

        switch (choice) {
            case 1:
                set_opening_cash();
                break;
            case 2:
                add_entry(INFLOW);
                break;
            case 3:
                add_entry(OUTFLOW);
                break;
            case 4:
                list_entries();
                break;
            case 5:
                list_entries_with_running_balance();
                break;
            case 6:
                edit_entry();
                break;
            case 7:
                delete_entry();
                break;
            case 8:
                show_cash_summary();
                break;
            case 9:
                show_category_summary();
                break;
            case 10:
                forecast_runway();
                break;
            case 11:
                running = 0;
                printf("Exiting program. Goodbye.\n");
                break;
            default:
                printf("Invalid choice. Try again.\n");
        }

        if (running) {
            pause_for_enter();
        }
    }

    return 0;
}